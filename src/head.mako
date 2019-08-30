<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
% if use_sw and sw:
<link rel="manifest" href="${copy('manifest.json')}" />
<meta name="theme-color" content="#99badd" />
% endif
% if embedcss:
<style>
  ${include('site.css')}
  ${include(css + '.css')}
</style>
% else:
<link rel="stylesheet" href="${copy('site.css')}" />
<link rel="stylesheet" href="${copy(css + '.css')}" />
% endif
<script type="module" src="${link(js + '.js')}"></script>
