"""Regression checks for numeric target spacing across the shared lens pipeline."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from types import SimpleNamespace

import torch

from tasks import TaskExample, get_task_spec
from evaluate_baseline import CandidateValues, tokenize_candidates, evaluate_batch
from evaluate_logit_lens import node_token_info, first_query_token_index, load_fx_catalog


class Tokenizer:
    """Separate spaces before digits, like the OLMo tokenizer."""
    pad_token_id = 0

    def encode(self, text, **kwargs):
        return [ord(c) for c in text]

    def decode(self, ids, **kwargs):
        if isinstance(ids, int):
            ids = [ids]
        return ''.join(chr(int(i)) for i in ids)

    def __call__(self, prompts, **kwargs):
        return {'input_ids': torch.tensor([self.encode(p) for p in prompts])}


class NumericFormattingTest(unittest.TestCase):
    def test_year_prompt_catalog_and_lens_labels_agree(self):
        spec = get_task_spec('book-author-birthyear')
        query = TaskExample('Book', 'Author', '1890')
        prompt = spec.render_prompt([TaskExample('Other', 'Writer', '1960')], query)
        self.assertTrue(prompt.endswith('Q: Book\nA: '))
        self.assertIn('A: 1960\n\n', prompt)
        tokenizer = Tokenizer()
        catalog = tokenize_candidates(tokenizer, CandidateValues(
            spec.dataset_task, ('Book',), ('Author',), ('1890',)
        ))
        self.assertEqual(tokenizer.decode(catalog['GFx'][0]['token_ids']), '1890')
        self.assertEqual(tokenizer.decode(catalog['Fx'][0]['token_ids']), ' Author')
        info = node_token_info(tokenizer, query.as_dict(), task=spec.dataset_task)
        self.assertEqual(info['GFx']['first_token'], '1')
        start = first_query_token_index(tokenizer, prompt, query.x)
        self.assertEqual(tokenizer.decode(tokenizer.encode(prompt)[start:]), 'Book\nA: ')

        class Model:
            def get_input_embeddings(self):
                return SimpleNamespace(weight=torch.zeros(1))

            def generate(self, input_ids, **kwargs):
                answer = torch.tensor([tokenizer.encode('1890\n\n')])
                return SimpleNamespace(
                    sequences=torch.cat((input_ids, answer), dim=1),
                    logits=[torch.zeros(1, 256)],
                )

        result = evaluate_batch(Model(), tokenizer, [{
            'task': spec.dataset_task, 'prompt': prompt, 'query': query.as_dict(),
        }], tokenized_candidates=catalog, top_ks=(1,), torch_module=torch)[0]
        self.assertTrue(result['evaluation']['exact_match'])
        self.assertEqual(result['evaluation']['label'], '1890')

    def test_numeric_intermediate_catalog_and_lens_agree(self):
        task = 'mod-twenty-times-two'
        tokenizer = Tokenizer()
        info = node_token_info(tokenizer, {'x': '123', 'Fx': '3', 'GFx': '6'}, task=task)
        self.assertEqual([info[n]['first_token'] for n in ('x', 'Fx', 'GFx')], ['1', '3', '6'])
        catalog = tokenize_candidates(tokenizer, CandidateValues(task, ('123',), ('3',), ('6',)))
        with TemporaryDirectory() as d:
            path = Path(d) / 'summary.json'
            path.write_text(json.dumps({'task': task, 'candidate_catalog': catalog}))
            self.assertEqual(load_fx_catalog(path, task=task, tokenizer=tokenizer), catalog['Fx'])
            catalog['Fx'][0]['token_ids'] = tokenizer.encode(' 3')
            path.write_text(json.dumps({'task': task, 'candidate_catalog': catalog}))
            with self.assertRaisesRegex(ValueError, 'tokenizer IDs changed'):
                load_fx_catalog(path, task=task, tokenizer=tokenizer)

    def test_stale_numeric_prompt_and_whitespace_target_rejected(self):
        spec = get_task_spec('book-author-birthyear')
        with self.assertRaisesRegex(ValueError, 'regenerate'):
            spec.validate_prompt('Q: Book\nA:', 'Book')
        with self.assertRaisesRegex(ValueError, 'whitespace'):
            spec.token_ids(Tokenizer(), 'GFx', ' 1890')

    def test_numeric_policy_is_per_node(self):
        spec = get_task_spec('word-int-times-two')
        self.assertEqual(spec.target_text('x', 'twelve'), ' twelve')
        self.assertEqual(spec.target_text('Fx', '12'), '12')
        self.assertEqual(spec.target_text('GFx', '24'), '24')
        for task in ('landmark-country-capital', 'park-country-capital'):
            spec = get_task_spec(task)
            self.assertEqual(spec.answer_prefix, 'A:')
            self.assertEqual(spec.target_text('Fx', 'Egypt'), ' Egypt')


if __name__ == '__main__':
    unittest.main()
