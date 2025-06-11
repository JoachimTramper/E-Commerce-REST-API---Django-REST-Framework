window.onload = function() {
  const ui = SwaggerUIBundle({
    url: "https://web-production-7c555.up.railway.app/api/schema/",
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
