import gradio as gr

from models import run_all_models
from scorer import calculate_strength


def percentile(score):
    if score >= 950:
        return "Top 1%"
    if score >= 850:
        return "Top 5%"
    if score >= 700:
        return "Top 10%"
    if score >= 500:
        return "Top 25%"
    return "Emerging Signal"


def strength_bar(score, width=25):
    filled = round((score / 1000) * width)
    filled = min(width, filled)
    empty = width - filled
    return "█" * filled + "░" * empty


def score_bar(score, width=20):
    filled = round((score / 100) * width)
    filled = min(width, filled)
    empty = width - filled
    return "█" * filled + "░" * empty


def analyze_person(name):
    if not name.strip():
        return "Please enter a name."
    results = run_all_models(name)
    metrics = calculate_strength(results)
    valid_descriptions = [
        d for d in results.values() if not d.startswith("ERROR")
    ]
    consensus = ""
    if valid_descriptions:
        consensus = max(valid_descriptions, key=len)
    strength_visual = strength_bar(metrics["strength"])
    report = f"""
# {name}

## Strength Score

**{metrics['strength']} strength · {percentile(metrics['strength'])}**

{strength_visual}

Recognized by **{metrics['recognized_models']}/{metrics['total_models']} models**

---

## Model Results

"""
    for model, description in results.items():
        score = metrics["model_scores"].get(model, 0)
        bar = score_bar(score)
        report += f"""
### {model}

**{bar} {score}/100**

{description}

"""
    return report


ARCADE_CSS = """
/* ── Import pixel / arcade font ─────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Share+Tech+Mono&display=swap');

/* ── Root palette  (Axecadia stripes) ───────────────────── */
:root {
    --axe-bg:       #1e1a17;   /* near-black cabinet body  */
    --axe-panel:    #2a2420;   /* slightly lighter panel   */
    --axe-cream:    #f0e8cc;   /* cabinet face / text      */
    --axe-yellow:   #f5c518;   /* top stripe               */
    --axe-orange:   #e07b20;   /* second stripe / primary  */
    --axe-red:      #c0392b;   /* third stripe             */
    --axe-maroon:   #7b1f2e;   /* bottom stripe            */
    --axe-outline:  #1a1208;   /* thick sticker outline    */
    --axe-dim:      #8a7a60;   /* subdued text             */
}

/* ── Global page ─────────────────────────────────────────── */
body, .gradio-container {
    background-color: var(--axe-bg) !important;
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--axe-cream) !important;
}

/* ── Stripe header bar (mimics cabinet base) ─────────────── */
.gradio-container::before {
    content: '';
    display: block;
    height: 6px;
    background: linear-gradient(
        to right,
        var(--axe-yellow)  0%   25%,
        var(--axe-orange)  25%  50%,
        var(--axe-red)     50%  75%,
        var(--axe-maroon)  75% 100%
    );
    margin-bottom: 0;
}

/* ── Main title markdown ─────────────────────────────────── */
.gradio-container .prose h1,
.gradio-container h1 {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 1.1rem !important;
    color: var(--axe-yellow) !important;
    text-shadow: 3px 3px 0px var(--axe-outline) !important;
    letter-spacing: 0.05em !important;
    line-height: 1.8 !important;
    margin-bottom: 0.5rem !important;
}

.gradio-container .prose h2,
.gradio-container h2 {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.65rem !important;
    color: var(--axe-orange) !important;
    letter-spacing: 0.08em !important;
    margin-top: 1.2rem !important;
}

.gradio-container .prose h3,
.gradio-container h3 {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem !important;
    color: var(--axe-yellow) !important;
    border-left: 3px solid var(--axe-orange);
    padding-left: 0.5rem;
    margin-top: 1rem !important;
}

.gradio-container .prose p,
.gradio-container p,
.gradio-container .prose li,
.gradio-container li {
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--axe-cream) !important;
    font-size: 0.8rem !important;
    line-height: 1.7 !important;
}

/* ── Card / block containers ─────────────────────────────── */
.gradio-container .block,
.gradio-container .gap,
.gradio-container .form {
    background: var(--axe-panel) !important;
    border: 2px solid var(--axe-outline) !important;
    border-radius: 4px !important;
}

/* ── Textbox ─────────────────────────────────────────────── */
.gradio-container input[type="text"],
.gradio-container textarea,
.gradio-container .scroll-hide {
    background: #120f0a !important;
    border: 2px solid var(--axe-orange) !important;
    border-radius: 3px !important;
    color: var(--axe-cream) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.9rem !important;
    caret-color: var(--axe-yellow);
    box-shadow: inset 0 0 8px rgba(224,123,32,0.15) !important;
}

.gradio-container input[type="text"]:focus,
.gradio-container textarea:focus {
    outline: none !important;
    border-color: var(--axe-yellow) !important;
    box-shadow: 0 0 10px rgba(245,197,24,0.3) !important;
}

/* Label */
.gradio-container label span,
.gradio-container .svelte-1gfkn6j {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.55rem !important;
    color: var(--axe-dim) !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── Buttons ─────────────────────────────────────────────── */
.gradio-container button.primary,
.gradio-container button[variant="primary"] {
    background: var(--axe-orange) !important;
    color: var(--axe-outline) !important;
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.1em !important;
    border: 3px solid var(--axe-outline) !important;
    border-radius: 3px !important;
    box-shadow: 4px 4px 0px var(--axe-outline) !important;
    transition: transform 0.08s, box-shadow 0.08s !important;
    text-transform: uppercase !important;
}

.gradio-container button.primary:hover,
.gradio-container button[variant="primary"]:hover {
    background: var(--axe-yellow) !important;
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px var(--axe-outline) !important;
}

.gradio-container button.primary:active,
.gradio-container button[variant="primary"]:active {
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0px var(--axe-outline) !important;
}

/* Clear button */
.gradio-container button.secondary {
    background: transparent !important;
    color: var(--axe-dim) !important;
    font-family: 'Press Start 2P', monospace !important;
    font-size: 0.55rem !important;
    letter-spacing: 0.08em !important;
    border: 2px solid var(--axe-maroon) !important;
    border-radius: 3px !important;
    box-shadow: 3px 3px 0px var(--axe-outline) !important;
    text-transform: uppercase !important;
    transition: border-color 0.1s, color 0.1s !important;
}

.gradio-container button.secondary:hover {
    border-color: var(--axe-red) !important;
    color: var(--axe-red) !important;
}

/* ── Output markdown area ────────────────────────────────── */
.gradio-container .prose {
    border: none !important;
    border-radius: 0 !important;
    padding: 0.5rem 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    overflow: visible !important;
}

.gradio-container .markdown-body,
.gradio-container [data-testid="markdown"] {
    overflow: visible !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

/* ── Horizontal rule in output ───────────────────────────── */
.gradio-container .prose hr {
    border: none !important;
    border-top: 2px dashed var(--axe-maroon) !important;
    margin: 1rem 0 !important;
}

/* ── Bold text in output ─────────────────────────────────── */
.gradio-container .prose strong {
    color: var(--axe-yellow) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── Bottom stripe footer ────────────────────────────────── */
.gradio-container::after {
    content: '';
    display: block;
    height: 5px;
    background: linear-gradient(
        to right,
        var(--axe-maroon) 0%   25%,
        var(--axe-red)    25%  50%,
        var(--axe-orange) 50%  75%,
        var(--axe-yellow) 75% 100%
    );
    margin-top: 2rem;
}

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--axe-bg); }
::-webkit-scrollbar-thumb { background: var(--axe-maroon); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--axe-orange); }
"""

with gr.Blocks(css=ARCADE_CSS, title="IN THE WEIGHTS") as demo:

    gr.Markdown(
        """
# IS THIS PERSON IN THE WEIGHTS?

Measure how strongly small language models can identify a person without external search.

Small models:
- Gemma 1B
- Llama 3.2 1B
- Qwen 0.6B

NOTE: 
- If the models don't recognize the person, it doesn't mean they aren't important. It just means they aren't widely known by these small models.
- The models are not perfect and may produce inaccurate or biased results. Use this tool for fun and exploration, not as a definitive measure of a person's significance.
- Outputs may take some time to generate, if the screen looks frozen, don't panic. Please be patient.
"""
    )

    name = gr.Textbox(
        label="Enter Person Name",
        placeholder="Elon Musk"
    )

    output = gr.Markdown()

    with gr.Row():
        btn = gr.Button(
            "Check",
            variant="primary"
        )
        clear_btn = gr.ClearButton(
            components=[name, output],
            value="Clear"
        )

    btn.click(
        fn=analyze_person,
        inputs=name,
        outputs=output,
    )

demo.launch()