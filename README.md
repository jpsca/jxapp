# Jx Component Viewer

Minimal app for quickly testing [Jx](https://jx.scaletti.dev/) components with TailwindCSS v4.

Built with Flask, [Hotwired Turbo](https://turbo.hotwired.dev/), and [Stimulus](https://stimulus.hotwired.dev/). Includes dark mode support.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
make install
```

## Run

```bash
make run
```

Then open http://127.0.0.1:6000/. The index page lists all available components.

## Adding components

1. Create a subfolder inside `display/`, e.g. `display/sidebar/`.
2. Add `.jinja` files to it, e.g. `display/sidebar/nav.jinja`.
3. Optionally add CSS, JS, or image files alongside the template.
4. Restart the dev server.

The component is now visible at the URL matching its path — `display/sidebar/nav.jinja` becomes `/sidebar/nav/`.

## Asset resolution

Declare assets in your component with `{#css filename.css #}` or `{#js filename.js #}` using just the filename. They are automatically resolved to `/<folder>/filename.css` based on the component's folder.

Static files in `display/<folder>/` are served directly at `/<folder>/`.

JS files are loaded as ES modules. Use `DOMContentLoaded` to run initialization code:

```js
document.addEventListener('DOMContentLoaded', () => {
  // setup here
});
```

## Component parameters

Use the `{#def #}` directive to declare parameters with defaults:

```jinja
{#css card.css #}
{#js card.js #}
{#def title="Example Card", description="A description." #}
<h2>{{ title }}</h2>
<p>{{ description }}</p>
```

## Example

An example component is included at `display/example/card.jinja` with accompanying CSS and JS assets.

## Project structure

```
app.py                  Flask application
templates/wrapper.html  Base HTML wrapper (dark mode, Tailwind, Turbo, Stimulus)
display/                Component directory (add your components here)
  example/              Example component
    card.jinja
    card.css
    card.js
static/                 Global assets (Tailwind, Turbo, Stimulus, app CSS/JS)
```

## License

MIT
