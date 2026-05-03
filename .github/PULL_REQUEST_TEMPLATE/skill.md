## Summary

<!-- What's the new/changed skill? -->

## Skill checklist

- [ ] `SKILL.md` has valid frontmatter (`name`, `description`)
- [ ] `name` ≤ 64 characters
- [ ] `description` clearly states when the skill should be invoked
- [ ] References under `references/` are loaded only on demand (progressive disclosure)
- [ ] Scripts under `scripts/` have shebangs and are executable
- [ ] Eval added/updated under `tests/evals/<plugin>/<skill>/`

## Testing

- [ ] `pytest tests/unit` passes
- [ ] `pytest tests/evals/<plugin>/<skill>` passes
- [ ] If skill behavior changed intentionally: baselines updated via
      `pytest tests/evals/<plugin>/<skill> --update-baselines`
- [ ] All commits are signed off (`git commit -s`)
