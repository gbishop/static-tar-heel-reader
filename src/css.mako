<%page args="name" />
<% fullname = name + ".css" %>
% if dev:
<link rel="stylesheet" href="${fullname}" />
% else:
  <style>
  <%include file="${fullname}" />
</style>
% endif
