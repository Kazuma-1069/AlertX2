---
name: AlertX Safety Core
colors:
  surface: '#111316'
  surface-dim: '#111316'
  surface-bright: '#37393d'
  surface-container-lowest: '#0c0e11'
  surface-container-low: '#1a1c1f'
  surface-container: '#1e2023'
  surface-container-high: '#282a2d'
  surface-container-highest: '#333538'
  on-surface: '#e2e2e6'
  on-surface-variant: '#e5bdb7'
  inverse-surface: '#e2e2e6'
  inverse-on-surface: '#2f3034'
  outline: '#ac8883'
  outline-variant: '#5c403b'
  surface-tint: '#ffb4a8'
  primary: '#ffb4a8'
  on-primary: '#690001'
  primary-container: '#d92d20'
  on-primary-container: '#fff6f5'
  inverse-primary: '#bc140d'
  secondary: '#8bceff'
  on-secondary: '#00344e'
  secondary-container: '#00a2e8'
  on-secondary-container: '#00344f'
  tertiary: '#ffb875'
  on-tertiary: '#4b2800'
  tertiary-container: '#a86000'
  on-tertiary-container: '#fff6f1'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad5'
  primary-fixed-dim: '#ffb4a8'
  on-primary-fixed: '#410000'
  on-primary-fixed-variant: '#930002'
  secondary-fixed: '#c9e6ff'
  secondary-fixed-dim: '#8bceff'
  on-secondary-fixed: '#001e2f'
  on-secondary-fixed-variant: '#004b6f'
  tertiary-fixed: '#ffdcc0'
  tertiary-fixed-dim: '#ffb875'
  on-tertiary-fixed: '#2d1600'
  on-tertiary-fixed-variant: '#6b3b00'
  background: '#111316'
  on-background: '#e2e2e6'
  surface-variant: '#333538'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 56px
    fontWeight: '800'
    lineHeight: 64px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '800'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: 0em
  title-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0em
  title-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
    letterSpacing: 0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0.01em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0.015em
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.05em
  timer-display:
    fontFamily: Inter
    fontSize: 64px
    fontWeight: '800'
    lineHeight: 68px
    letterSpacing: -0.03em
  timer-display-mobile:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 52px
    letterSpacing: -0.03em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-mobile: 0.75rem
  margin: 1.5rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system delivers an authoritative, instantaneous, and mission-critical public safety environment. Designed for high-stress, rapid-decision contexts, the aesthetic merges Modern Tactical Functionalism with Google Material 3 and KivyMD architectural patterns. It avoids non-essential decorative styling in favor of absolute visual clarity, swift comprehension, and reliable physical targets.

The interface projects steady competence, reassurance, and decisive urgency. Its primary audience spans citizens in distress, emergency family contacts, and field responders who demand rapid navigation under adverse lighting, motion, and psychological pressure. The design style relies on high-contrast surface tiers, tactile micro-affordances, and strict semantic color isolation—ensuring life-critical actions like SOS triggers are instantly recognizable while preventing cognitive exhaustion during routine safety monitoring.

## Colors

The system uses an intentional dark-mode-first foundation to preserve battery during critical events, minimize screen glare in night-time emergencies, and provide maximum contrast for life-critical alerts.

### Palette Architecture
- **Critical / SOS Red (`#D92D20`)**: The primary brand anchor, reserved exclusively for active emergencies, urgent triggers, and destructive safety actions. Never diluted on secondary navigation or low-priority statuses. Its paired beacon glow (`#EF4444`) is limited to radiating ring states and active distress toggles.
- **Info / Tracking Blue (`#0BA5EC`)**: The secondary anchor, governing geolocation relays, breadcrumb paths, active radar rings, and navigation vectors.
- **Warning / Timer Amber (`#F79009`)**: Tertiary signal dedicated to safety check-in countdowns, delayed trigger alerts, and low-connectivity warnings.
- **Safe / Resolved Green (`#12B76A`)**: Isolated semantic token indicating secure zones, confirmed check-ins, and resolved status checks.
- **Neutral Core**:
  - `Canvas Dark`: `#121417` (True ambient contrast floor)
  - `Surface Level 1`: `#1E2228` (Base structural cards and sheets)
  - `Surface Level 2`: `#2B303A` (Elevated components, floating sheets, inputs)
  - `Surface High Contrast Light`: `#F4F6F8` (Primary typography, icon fills, and optional inverted light-mode substrate)

### Functional Distribution
Semantic colors are strictly transactional. Informational screens maintain 85% neutral dominance (`#121417` to `#2B303A`) with `#F4F6F8` text hierarchy. Critical alerts break through this base with full-intensity `#D92D20` flood fills and synchronized feedback.

## Typography

Typography centers on total legibility across compromised conditions—shaking hands, bright sunlight, cracked screens, or moving transit. `Inter` provides neutral, grotesque geometry with tall x-height, open apertures, and disambiguated glyph shapes.

### Scaling & Legibility Rules
- **Countdown & Metrics Hierarchy**: The `timer-display` and `display-lg` levels use tabular figures (`tnum`) to eliminate spatial shifting during dynamic countdowns.
- **Minimum Enforced Size**: No readable instructional copy falls below `body-md` (14px). Labels below 14px are reserved strictly for auxiliary metadata, tracking stamps, or badge counts.
- **Weight Pairing**: Headers and critical actions leverage heavy weights (600–800) to stand out sharply against deep charcoal card surfaces.

## Layout & Spacing

The layout operates on a standard 8-point vertical grid (augmented by a 4-point micro-step). Spacing reinforces rapid touch accuracy, avoiding cluttered grouping and accidental miss-presses.

### Screen Structure & Safe Areas
- **Mobile Handheld Frame (Base)**: Single-column fluid layout with an outer canvas margin of `1rem` (16px) extending to `1.5rem` (24px) on wider displays.
- **Touch Target Enforcements**: All actionable components maintain a minimum physical target size of 48px × 48px. The primary SOS zone utilizes a minimum 96px to 140px target diameter centered in the bottom two-thirds thumb reach zone.
- **Adaptive Breakpoints**:
  - `Compact (<600px)`: Single column, sticky bottom navigation, bottom-docked SOS action cards.
  - `Medium (600px–1023px)`: Two-column asymmetrical dashboard (65% situational map/status, 35% action feed).
  - `Expanded (≥1040px)`: Three-column emergency center with fixed navigation rail, central telemetry, and right-hand responder logistics.

## Elevation & Depth

Elevation in this design system is achieved through tonal separation rather than drop shadows. It relies on luminance stepping inspired by KivyMD and Material 3, layered with subtle structural rim outlines.

### Tonal Tiers
- **Tier 0 (Base Canvas)**: `#121417`. Deepest background surface.
- **Tier 1 (Surface Cards & Low-Priority Panels)**: `#1E2228`. Structural cards, lists, and inactive navigation bars. Outlined by an ultra-thin 1px border (`rgba(244, 246, 248, 0.08)`).
- **Tier 2 (Elevated Modals, Active Cards, Menus)**: `#2B303A`. Overlaid cards, active inputs, and interactive dialogs.
- **Tier 3 (Floating Emergency Modules)**: `#2B303A` paired with a directional diffuse glow. For SOS alerts, an ambient critical crimson halo (`0 0 32px rgba(239, 68, 68, 0.35)`) projects emergency status without creating visual noise.

Drop shadows are avoided on standard controls to keep screens crisp in low-light environments.

## Shapes

The shape language utilizes smooth, ergonomic curvatures (Level 2) that feel modern and approachable while maintaining functional discipline.

### Geometric Application
- **Core Cards (MDCard pattern)**: `1rem` (16px) corner radius for small/medium utility cards; `1.5rem` (24px) for prominent alert containers and parent panels.
- **Buttons & Input Fields**: `0.75rem` (12px) to `1rem` (16px) continuous corner radiuses providing a stable target shape.
- **SOS Main Action Button**: Perfect circular profile (`9999px`) reinforced by concentric circular pulse boundary rings.
- **Status Badges & Micro Chips**: Fully rounded pill shapes (`9999px`) to visually differentiate status tokens from squircle interaction surfaces.

## Components

### 1. The Central Tactical SOS Button
- **Structure**: Concentric multi-layer circular component (120px base diameter on mobile). 
- **Resting State**: Solid `#D92D20` core with a centered high-contrast white distress glyph, encased in a `#1E2228` outer ring with a 1px border (`rgba(217, 45, 32, 0.4)`).
- **Active / Triggering State**: Smooth physical-press scale down (0.94) accompanied by two radiating, expanding ripple rings using `#EF4444` at decreasing opacity (30% down to 0%).
- **Interaction Model**: Supports immediate press-and-hold (3-second default) to prevent false-positives, displaying an animated clockwise radial fill line along the border.

### 2. Buttons
- **Primary Danger / Action**: Background `#D92D20`, text `#F4F6F8`, height 52px, corner radius 16px. Font weight 600.
- **Secondary Neutral**: Background `#2B303A`, text `#F4F6F8`, 1px border `rgba(244, 246, 248, 0.12)`, height 52px.
- **Ghost / Tertiary**: Transparent background, text `#0BA5EC` or `#F4F6F8`, minimum touch target padding 12px × 16px.

### 3. Cards (MDCard Adaptations)
- **Standard Telemetry Card**: Background `#1E2228`, border radius 16px, 1px perimeter stroke of `rgba(244, 246, 248, 0.06)`, internal padding `1.25rem` (20px).
- **Critical Alert Card**: Background `#1E2228` with an authoritative 4px solid left border in `#D92D20`. Top-level header contains the status chip and clear dismissal/action controls.

### 4. Chips & Status Badges
- **Pill Formation**: Height 28px–32px, radius 9999px, padding 4px 12px.
- **Variants**:
  - *Emergency Active*: Background `rgba(217, 45, 32, 0.15)`, text `#D92D20`, border 1px solid `#D92D20`.
  - *Safe / Clear*: Background `rgba(18, 183, 106, 0.15)`, text `#12B76A`, border 1px solid `#12B76A`.
  - *Warning Timer*: Background `rgba(247, 144, 9, 0.15)`, text `#F79009`, border 1px solid `#F79009`.
  - *Tracking / Info*: Background `rgba(11, 165, 236, 0.15)`, text `#0BA5EC`, border 1px solid `#0BA5EC`.

### 5. Input Fields
- **Container**: Background `#1E2228`, height 56px, radius 12px, border 1.5px solid `rgba(244, 246, 248, 0.12)`.
- **Focus State**: Border color transitions to `#0BA5EC` with zero drop shadow to maintain clean readability.
- **Typography**: Input text `#F4F6F8` (16px), label `#F4F6F8` at 60% opacity resting inside top edge on focus.

### 6. High-Contrast Bottom Navigation Bar
- **Dimensions & Specs**: Fixed height 68px (plus mobile device safe area bottom inset), background `#1E2228`, 1px solid top border `rgba(244, 246, 248, 0.08)`.
- **Items (5 Distinct Tabs)**: Home, Safety, Guides, Contacts, Profile.
- **Item States**:
  - *Active*: Top-level icon tinted `#F4F6F8` resting over a subtle Pill indicator (`#2B303A`), label in `label-md` bold `#F4F6F8`.
  - *Inactive*: Icon and label tinted `rgba(244, 246, 248, 0.45)`.
- **Target Spacing**: Equal width distribution (20% per slot) with centered 48px vertical touch zones.

### 7. Safety Check-In Countdowns & Timers
- Standalone card pairing a high-visibility countdown string (`timer-display`) with an Amber `#F79009` linear progress bar across the card's top edge. Features immediate two-tap cancellation or manual check-in resolution buttons.