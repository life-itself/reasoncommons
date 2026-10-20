// Seeded defects: known failures applied to a rendered candidate so the evaluator's sensitivity can be checked.
// They change only the captured browser state; candidate files, registry hashes and sources stay untouched.

export const FALSE_CLAIM = 'Reason Commons connects to Discord, Slack and Microsoft Teams today, and teams using it make measurably better decisions.';

export const DEFECTS = {
  'remove-install': {
    description: 'Removes every try/install control and every visible install command.',
    expect: 'The scripted main-action probe reports not-found or fail, never pass.',
    apply: ({ pattern, install_command }) => {
      const re = new RegExp(pattern, 'i'), cmd = new RegExp(install_command);
      let removed = 0;
      for (const el of [...document.querySelectorAll('a, button, [role=button]')]) {
        if (el.isConnected && re.test(el.innerText || el.getAttribute('aria-label') || '')) { el.remove(); removed++; }
      }
      const holders = [...document.body.querySelectorAll('*')].filter(el => cmd.test(el.textContent || '') && ![...el.children].some(child => cmd.test(child.textContent || '')));
      for (const el of holders) if (el.isConnected) { (el.closest('pre, p, li') || el).remove(); removed++; }
      return { removed };
    }
  },
  'false-claim': {
    description: 'Inserts a capability and outcome claim that the supplied facts contradict, directly after the main headline.',
    expect: 'The inserted claim appears in captured text; a judge should report a factual error citing discourse-annotation-prototyped, self-use-only or evidence-limit.',
    contradicts: ['discourse-annotation-prototyped', 'self-use-only', 'evidence-limit'],
    apply: ({ claim }) => {
      const p = document.createElement('p');
      p.textContent = claim;
      p.setAttribute('data-seeded-defect', 'false-claim');
      const h1 = document.querySelector('h1');
      if (h1) h1.insertAdjacentElement('afterend', p); else document.body.prepend(p);
      return { inserted: claim, after_headline: !!h1 };
    }
  },
  'bury-headline': {
    description: 'Moves the main headline to the end of the page.',
    expect: 'The headline text is absent from the captured first screen; a first-screen judge should explain the page less well.',
    apply: () => {
      const h1 = document.querySelector('h1');
      if (!h1) return { moved: null };
      document.body.append(h1);
      return { moved: h1.innerText.trim() };
    }
  }
};

export function parseDefects(value) {
  const ids = value === true || !value ? Object.keys(DEFECTS) : String(value).split(',');
  for (const id of ids) if (!DEFECTS[id]) throw new Error(`Unknown seeded defect ${id}. Use ${Object.keys(DEFECTS).join(', ')}.`);
  return ids;
}

export async function applyDefect(frame, id, config) {
  const defect = DEFECTS[id];
  const args = { ...config.capture.main_action, claim: FALSE_CLAIM };
  return { id, description: defect.description, expect: defect.expect, result: await frame.evaluate(defect.apply, args) };
}
