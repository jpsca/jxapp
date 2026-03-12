# Jx Component Viewer

Minimal app for quickly testing [Jx](https://jx.scaletti.dev/) components with TailwindCSS v4.

## Setup

```bash
uv sync
```

## Run

```bash
make run
```

Then open http://127.0.0.1:5000/. The index page lists all available components.

## Adding components

1. Create a subfolder inside `display/`, e.g. `display/sidebar/`.
2. Add `.jinja` files to it, e.g. `display/sidebar/nav.jinja`.
3. Optionally add an `assets/` subfolder with CSS, JS, or images: `display/sidebar/assets/`.
4. Restart the dev server.

The component is now visible at the URL matching its path — `display/sidebar/nav.jinja` becomes `/sidebar/nav/`.

## Asset resolution

Declare assets in your component with `{#css filename.css #}` or `{#js filename.js #}` using just the filename. They are automatically resolved to `/assets/<folder>/filename.css` based on the component's folder.

Static files in `display/<folder>/assets/` are served at `/assets/<folder>/`.

JS files are loaded as ES modules. Use `DOMContentLoaded` to run initialization code:

```js
document.addEventListener('DOMContentLoaded', () => {
  // setup here
});
```

## Example

An example component is included at `display/example/card.jinja` with accompanying CSS and JS assets.
