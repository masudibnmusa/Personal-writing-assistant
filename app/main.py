"""
Entry point for the Personal Writing Assistant (CLI).
"""
import argparse
import sys

from app.config import load_config
from app.style_engine.sample_collector import collect_samples
from app.style_engine.style_analyzer import analyze_style
from app.style_engine.style_profile import save_profile, load_profile
from app.generation.prompt_builder import build_prompt
from app.generation.llm import generate_content
from app.generation.content_types import CONTENT_TYPES


def cmd_analyze(args):
    samples = collect_samples(args.samples_dir)
    profile = analyze_style(samples)
    save_profile(profile, args.profile_name)
    print(f"Style profile saved as '{args.profile_name}'")


def cmd_generate(args):
    profile = load_profile(args.profile_name)
    prompt = build_prompt(
        profile=profile,
        content_type=args.type,
        instructions=args.instructions,
    )
    output = generate_content(prompt)
    print("\n--- Generated Draft ---\n")
    print(output)


def main():
    parser = argparse.ArgumentParser(description="Personal Writing Assistant")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze_p = sub.add_parser("analyze", help="Build a style profile from writing samples")
    analyze_p.add_argument("--samples-dir", default="data/writing_samples")
    analyze_p.add_argument("--profile-name", default="default")
    analyze_p.set_defaults(func=cmd_analyze)

    gen_p = sub.add_parser("generate", help="Generate content in your style")
    gen_p.add_argument("--profile-name", default="default")
    gen_p.add_argument("--type", choices=list(CONTENT_TYPES.keys()), default="email")
    gen_p.add_argument("--instructions", required=True, help="What to write about")
    gen_p.set_defaults(func=cmd_generate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())