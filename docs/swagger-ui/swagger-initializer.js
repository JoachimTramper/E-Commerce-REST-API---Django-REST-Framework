window.onload = function() {
  const ui = SwaggerUIBundle({
    url: "/schema.yml",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    layout: "BaseLayout",
    tryItOutEnabled: true,
  });
  window.ui = ui;
};
