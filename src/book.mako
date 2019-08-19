<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="stylesheet" href="${css}" />
    <script src="${js}"></script>
    <title>${title}</title>
  </head>

  <body id="${bid}">
    % for page in pages:
    <section id="${page['id']}">
      % if 'pageno' in page:
      <span>${page['pageno']}</span>
      % endif
      % if 'author' in page:
      <h1>${page['title']}</h1>
      <p id="author">${page['author']}</p>
      % endif
      <img src="${page['image']}" />
      % if 'text' in page:
      <p>${page['text']}</p>
      % endif
      <a class="back" href="${page['back']}">Back</a>
      <a class="next" href="${page['next']}">Next</a>
    </section>
    % endfor

    <section id="done">
      <a href="${start}">Read this book again</a>
      <a href="${index}">Read another book</a>
    </section>
  </body>
</html>
