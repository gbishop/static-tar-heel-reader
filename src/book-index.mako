<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="stylesheet" href="${css}" />
    <title>${name}</title>
  </head>

  <body>
    <ul>
      % for book in books:
      <li id="${book['id']}" class="${book['icons']}">
        <a href="${book['link']}.html#p1">
          <h1>${book['title']}</h1>
          <p>${book['author']}</p>
          <img src="${book['image']}" />
          <span>${book['pages']}</span>
        </a>
      </li>
      % endfor
    </ul>
    % if back:
    <a class="back" href="${back}">Back</a>
    % endif
    % if next:
    <a class="next" href="${next}">Next</a>
    % endif
  </body>
</html>
