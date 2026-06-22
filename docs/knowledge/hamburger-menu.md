# Hamburger Menu (Mobile Navigation)

## Implementation
- **Trigger**: screens ≤ 750px
- **CSS classes**: `.hamburger`, `.mobile-nav`, `.mobile-lang`
- **Toggle**: inline `onclick` toggles `.open` class on both `.hamburger` and `.mobile-nav`
- **Animation**: hamburger lines rotate into X when `.open`

## Structure (in every non-redirect HTML page)
```html
<!-- Inside .header-inner, after .lang-switcher -->
<button class="hamburger" onclick="document.querySelector('.hamburger').classList.toggle('open');document.querySelector('.mobile-nav').classList.toggle('open')" aria-label="Menu">
  <span></span><span></span><span></span>
</button>

<!-- Immediately after </header> -->
<div class="mobile-nav">
  <a href="...">Home</a>
  <a href="..." class="active">Current Page</a>
  <a href="...">Other Page</a>
  <div class="mobile-lang">
    <!-- Same lang-btn buttons as desktop -->
  </div>
</div>
```

## Responsive Behavior
- Desktop: `.hamburger { display: none; }`, `.nav-links` and `.lang-switcher` visible
- Mobile: `.hamburger { display: flex; }`, `.nav-links` and `.lang-switcher` hidden, `.mobile-nav` shown on `.open`

## Pages with hamburger (27 total)
All non-redirect HTML files. The 5 redirect files (`[lang]/credit-cards/index.html` for non-JA) are excluded.

## Notes
- Each page's mobile-nav has page-specific links and active states
- Lang switcher in mobile-nav mirrors the desktop lang-switcher exactly
- The mobile-nav is a fixed overlay (`position: fixed; top: 56px`) covering the full viewport
