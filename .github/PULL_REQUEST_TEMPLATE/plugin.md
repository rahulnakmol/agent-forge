## Summary

<!-- What's the new plugin and what does it do? -->

## Plugin checklist

- [ ] Added under `plugins/<my-plugin>/` with `.claude-plugin/plugin.json`
- [ ] Registered in `.claude-plugin/marketplace.json`
- [ ] Includes at least one skill under `skills/<name>/SKILL.md`
- [ ] At least one Layer B eval under `tests/evals/<my-plugin>/`
- [ ] Eval baselines committed (`tests/evals/_baseline_scores.json`)

## License attestation

- [ ] All third-party assets (fonts, templates, references) are listed in
      `plugins/<my-plugin>/THIRD_PARTY_NOTICES.md` with their licenses
- [ ] All assets are BSD-compatible or Apache-2.0 / MIT / public domain
- [ ] No KPMG or other proprietary brand assets

## Testing

- [ ] `pytest tests/unit -k <my-plugin>` passes
- [ ] `pytest tests/evals/<my-plugin>` passes
- [ ] All commits are signed off (`git commit -s`)
