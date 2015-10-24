var request = require('request');
var handlebars = require('handlebars');

var project = 'distractedness';
var url = 'http://devpost.com/software/' + project;
var api = 'https://iii3mdppm7.execute-api.us-east-1.amazonaws.com/prod/ProjectEndpoint/' + project;
var source = "<h2>{{title}}</h2><p>{{tagline}}</p><ul>{{#collaborators}}<li> <img src='{{avatar_url}}'> {{name}}</li>{{/collaborators}}</ul><ul>{{#built_with}}<li> #{{name}}</li>{{/built_with}}</ul>";

request({url: api, json: true}, function(err, res, json) {
  if (err) {throw err;}
  //var data = json;
  //console.log(data.title, data.tagline, data.collaborators, data.built_with);
  var template = handlebars.compile(source);
  var html = template(json);

  console.log(html);

});
