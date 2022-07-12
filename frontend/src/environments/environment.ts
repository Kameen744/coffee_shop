/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000/api/v1', // the running FLASK api server url
  auth0: {
    url: 'dev-083t87re.us', // the auth0 domain prefix
    audience: 'http://127.0.0.1:5000/api', // the audience set for the auth0 app
    clientId: 'MaAsY9B5SmFzc3YM6uREExs06PsQ6Ysm', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
