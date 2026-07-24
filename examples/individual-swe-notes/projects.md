# Side project: decision log

Problem: our team relitigates the same three or four decisions every
few months, because nobody can find *why* we decided something the
last time — only that we did. Slack search finds the messages but not
the reasoning, and reasoning is what actually changes minds.

Plan: a lightweight tool where a decision gets a stable ID, a
one-paragraph rationale, the alternatives considered, and a status
(proposed / adopted / revisited / superseded-by). Nothing fancy —
closer to an ADR (architecture decision record) than a wiki. The bet
is that most of the pain isn't the software, it's that nobody owns
writing the rationale down, so the format has to make that the
five-minute path, not the twenty-minute one.

Success looks like: three months from now, when someone asks "didn't
we already talk about this?", the answer is a link, not a shrug.
