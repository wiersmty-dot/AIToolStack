# Animation & Design Skills

A collection of Claude Code skills for web animation, motion design, and 3D/WebGL
work, vendored into this repository under `.claude/skills/`. Claude Code loads any
skill placed here automatically and activates it when a task matches the skill's
`description` triggers.

## Skills included

**25 skills** spanning the animation/design stack:

| Area | Skills |
|------|--------|
| 2D / JS animation | `animejs`, `animejs-v4`, `motion-framer`, `react-spring-physics`, `lottie-animations`, `rive-interactive`, `animate` |
| Scroll & transitions | `gsap-scrolltrigger`, `locomotive-scroll`, `scroll-reveal-libraries`, `barba-js` |
| 3D / WebGL | `threejs-webgl`, `react-three-fiber`, `babylonjs-engine`, `playcanvas-engine`, `aframe-webxr`, `pixijs-2d`, `lightweight-3d-effects` |
| 3D authoring pipeline | `blender-web-pipeline`, `substance-3d-texturing`, `spline-interactive` |
| Components & design | `animated-component-libraries`, `modern-web-design`, `web3d-integration-patterns` |
| Tooling | `skill-creator` |

## Sources

These skills were downloaded from the following open-source repositories:

- **[freshtechbro/claudedesignskills](https://github.com/freshtechbro/claudedesignskills)** (MIT) —
  provides the bulk of the set: Three.js, GSAP/ScrollTrigger, React Three Fiber,
  Motion (Framer Motion), Babylon.js, and the rest of the design/3D stack. Vendored
  from the repo's `.claude/skills/` tree (the redundant per-skill `.zip` distribution
  archives were intentionally excluded).
- **[delphi-ai/animate-skill](https://github.com/delphi-ai/animate-skill)** —
  installed as `animate/`. Next.js/React animation patterns (CSS, Framer Motion,
  easing, performance, accessibility) based on Emil Kowalski's "Animations on the Web".
- **[BowTiedSwan/animejs-skills](https://github.com/BowTiedSwan/animejs-skills)** —
  installed as `animejs-v4/` (its frontmatter `name` was renamed from `animejs` to
  `animejs-v4` to avoid colliding with the `animejs` skill from claudedesignskills).
  A dedicated, deeper Anime.js v4 reference.

### Source not used

- **claudskills.com** (`https://claudskills.com/skills/animations/SKILL.md`) — the
  install URL referenced in the original "skills.sh" post returns **HTTP 403** and
  could not be downloaded, so it was skipped.

## Notes on the original "5 animation skills" post

The marketing post listed five slide categories. Mapping them to what is actually
available open-source:

- *UI-Animation / Animation Designer* (page transitions, parallax, micro-interactions)
  → `modern-web-design`, `motion-framer`, `gsap-scrolltrigger`, `barba-js`,
  `locomotive-scroll`, `scroll-reveal-libraries`, `animate`
- *CSS Animations* → `animate` (CSS animations reference), `animejs`/`animejs-v4`
- *Three.js 3D Animation* → `threejs-webgl`, `react-three-fiber`, `web3d-integration-patterns`
- *Flutter Animations* → **no open-source skill found**; not included (these skills
  target the web platform, not Flutter/Dart).

## Installing globally instead

To use any of these outside this repo, copy a skill directory into your user-level
skills folder, e.g.:

```bash
cp -r .claude/skills/threejs-webgl ~/.claude/skills/
```
