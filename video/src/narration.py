"""Narration script — each chunk becomes one TTS clip / one timeline block."""

CHUNKS = [
    dict(id="c01_hook", slides=[("01_hero.png", 0.42), ("02_agenda.png", 0.58)], text=(
        "Hey what's up guys, it's Geoid back with another video. Today in this video, we are going to be "
        "talking about EverFunded, and more specifically, how its three account types actually compare, so "
        "you can pick the one that fits the way you trade. We're breaking down the 2-Step, the 1-Step and "
        "the Instant with the real numbers: profit targets, loss limits, qualifying days, fees, and the "
        "dashboard you'll actually see when you start. I'll walk you through it all on screen, and yes, I've "
        "got a launch code that gets you fifty percent off your first eligible purchase, so stick around to "
        "the end. Here's the plan, in order: the three accounts side by side, a deep dive on the 2-Step "
        "with a one hundred thousand dollar walkthrough, the trade-off versus the 1-Step, the Instant, then "
        "sizes and fees, the dashboard, which one I'd pick, and exactly how to claim the offer.")),
    dict(id="c02_overview", slides=[("03_overview.png", 1.0)], text=(
        "EverFunded offers simulated trading accounts up to two hundred thousand dollars, with payouts paid "
        "in twenty-four hours and a profit split of up to one hundred percent. You trade a simulated "
        "account, and the rewards you withdraw are real. There are three routes to get there. The 2-Step is "
        "a structured evaluation made of two phases, and it gives you wider loss limits. The 1-Step is a "
        "single phase to funded, with tighter loss limits. And the Instant starts you directly as a "
        "simulated funded account, no evaluation at all. Same firm, same platforms, same payout promise, "
        "three very different ways to trade it. We'll use the 2-Step as our main example, then show you "
        "exactly how the 1-Step and the Instant differ.")),
    dict(id="c03_twostep", slides=[("04_two_step.png", 0.46), ("05_two_step_math.png", 0.54)], text=(
        "Let's take the 2-Step as our main example, because it's the one most traders end up choosing. Two "
        "evaluation phases. Phase one has an eight percent profit target, phase two has five percent. Your "
        "maximum daily loss is five percent, and the static maximum overall loss is ten percent, measured "
        "from your initial balance. There's no deadline to hit those targets, subject to inactivity rules, "
        "and you need at least three qualifying trading days in each phase, where each qualifying day "
        "requires at least half a percent of realized net profit after trading costs. Here's the concrete "
        "math on a one hundred thousand dollar account. Phase one target: eight thousand dollars. Phase two "
        "target: five thousand. Your overall loss floor during the evaluation sits at ninety thousand "
        "dollars, ten percent below where you started, and it stays there. Each phase also starts again at "
        "one hundred thousand, so evaluation profits don't carry over into the next account. There's no "
        "consistency rule in the challenge, and once funded your best day just needs to stay under "
        "thirty-five percent of total profit.")),
    dict(id="c04_tradeoff", slides=[("06_tradeoff.png", 1.0)], text=(
        "Now, the useful comparison. The 2-Step gives you two phases, but wider loss limits than the "
        "1-Step. So you're trading a longer path to funded for more room to breathe on any given day. Think "
        "of it like this: if your strategy needs space to recover from a rough week, the 2-Step's ten "
        "percent overall and five percent daily limits give you that. If you want the shortest possible "
        "route and you trade tight, the 1-Step's limits force discipline. That's the trade-off, and it "
        "isn't about which account is best for everyone. It's about which constraint you'd rather live "
        "with: more time and more room, or one shot with tighter discipline.")),
    dict(id="c05_onestep", slides=[("07_one_step.png", 1.0)], text=(
        "The 1-Step is a single evaluation phase. One phase, ten percent profit target. Maximum daily loss "
        "of three percent, and a six percent static maximum overall loss, half the overall room of the "
        "2-Step. Again, no evaluation deadline, subject to inactivity rules, with the same qualifying "
        "requirement: at least three qualifying trading days, each with at least half a percent realized "
        "net profit after costs. The main advantage is the single-phase structure. You only have to pass "
        "once, and you go from evaluation to funded in a single step. The cost of that is tighter loss "
        "limits, both daily and overall, so there's far less room for a bad day.")),
    dict(id="c06_instant", slides=[("08_instant.png", 0.55), ("09_trailing.png", 0.45)], text=(
        "Then there's the Instant. No evaluation phase at all. You start directly as a simulated funded "
        "account. Maximum daily loss is three percent, and the overall limit is six percent trailing. "
        "Trailing means the limit follows your closed-balance highs: as your closed profits push the "
        "high-water mark up, the allowed loss floor moves up with it, and it eventually locks at your "
        "starting balance. So the better you do, the more protection you have, but a payout resets the "
        "balance and re-arms the trailing limit for the next cycle. Payout eligibility conditions still "
        "apply. This is the one that appeals to traders who would rather not sit through an evaluation "
        "before they can trade like a funded trader.")),
    dict(id="c07_sizes", slides=[("10_sizes.png", 1.0)], text=(
        "Six account sizes, from five thousand up to two hundred thousand. As an example, the one hundred "
        "thousand 2-Step has a one-time fee of five hundred sixty-two dollars and fifty cents, and with "
        "the launch code, that drops to two hundred eighty-one dollars and twenty-five cents. A five "
        "thousand account is forty-three seventy-five, or about twenty-two with the code. Leverage is one "
        "to one hundred during the 2-Step evaluation and one to fifty once funded; the other products run "
        "one to thirty. Gold, indices and oil are one to ten, crypto one to two. Platforms are Match-Trader "
        "and MetaTrader five, with the first payout after fourteen days and a minimum payout of one hundred "
        "dollars. There's also an optional add-on that raises your profit split from eighty percent to a "
        "full hundred percent.")),
    dict(id="c08_dashboard", slides=[("@clip:dashboard_demo", 0.5), ("12_objectives.png", 0.5)], text=(
        "So what do you actually see when you start? Let me walk you through it, live on screen. This is the "
        "real trader dashboard on app.everfunded.com, on an active one hundred thousand dollar 2-Step Phase "
        "one account. Right at the top you've got your account identity, the plan type and your two loss "
        "numbers. Under Risk Floors you can watch your static maximum loss anchored to the ninety thousand "
        "dollar floor, and your daily loss limit with its reset timer. Under Progress and Timelimits sits "
        "your profit target with the amount still to go, your qualifying days counter, and the inactivity "
        "rule. Scroll down and you've got your balance and equity curve with the target lines drawn in, "
        "analytics on what's making and costing you money, and the full trade history. And you can jump "
        "straight into Match-Trader from the same page, without leaving the dashboard.")),
    dict(id="c09_pick", slides=[("13_pick.png", 1.0)], text=(
        "So which one would I pick? Honestly, if I were starting today, I'd go with the 2-Step on a size I "
        "can actually trade well. The wider daily and overall loss limits give you room to have a bad day "
        "without ending the account, and there's no deadline breathing down your neck. That combination is "
        "worth more to me than saving one phase. If you're confident and want the shortest route to funded, "
        "the 1-Step is clean, but those three percent daily and six percent overall limits are unforgiving; "
        "one rough session can end it. And if you flat-out don't want an evaluation, the Instant gets you "
        "trading immediately, as long as you respect the trailing limit and the payout conditions.")),
    dict(id="c10_cta", slides=[("14_cta.png", 0.45), ("15_recap.png", 0.55)], text=(
        "Right, here's the offer. Pick the challenge that fits your trading style through my link in the "
        "description, and use the code GEOID at checkout for fifty percent off your first eligible purchase "
        "during the launch offer. Compare the accounts, review the rules, and choose the option that fits "
        "how you actually trade. The link and the code are right below the like button. Quick recap: "
        "2-Step, two phases, eight and five percent targets, five percent daily loss, ten percent static "
        "overall loss, so wider room. 1-Step, one phase, ten percent target, three percent daily, six "
        "percent static: shortest path, tightest limits. Instant, no evaluation, three percent daily, six "
        "percent trailing overall. Six sizes up to two hundred thousand, payouts in twenty-four hours, "
        "profit split up to one hundred percent. If you found this useful, hit like, subscribe with "
        "notifications on, and comment which account you'd pick. Trade safe, I'll see you in the next one.")),
]

if __name__ == "__main__":
    total = sum(len(c["text"].split()) for c in CHUNKS)
    print(f"{len(CHUNKS)} chunks, {total} words, ~{total/155*60:.0f}s at 155wpm")
    for c in CHUNKS:
        print(f"  {c['id']}: {len(c['text'])} chars")
