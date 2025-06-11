window.onload = function() {
  const ui = SwaggerUIBundle({
    url: "/api/schema/",
    dom_id: '#swagger-ui',
    supportedSubmitMethods: ['get','post','put','delete','patch'],
    validatorUrl: null,
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    layout: "StandaloneLayout",
  });
  window.ui = ui;
};
