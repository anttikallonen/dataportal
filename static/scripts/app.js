'use strict';

/**
 * @ngdoc overview
 * @name dataportalApp
 * @description
 * # dataportalApp
 *
 * Main module of the application.
 */
var app = angular
  .module('dataportalApp', [
    'ngAnimate',
    'ngAria',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngMaterial',
    'ngMdIcons',
    'ngFileUpload'
  ])
  .config(function ($routeProvider, $mdThemingProvider, $httpProvider)  {
    // initialize get if not there
    if (!$httpProvider.defaults.headers.get) {
        $httpProvider.defaults.headers.get = {};
    }
    // disable IE ajax request caching
    $httpProvider.defaults.headers.get['If-Modified-Since'] = 'Mon, 26 Jul 1997 05:00:00 GMT';
    // extra
    $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
    $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';

    $httpProvider.interceptors.push(function($location, $q, $window) {
  return {

            'responseError': function(rejection){
                var defer = $q.defer();
                if(rejection.status == 401){
                    $location.path('/login');
                }
                defer.reject(rejection);
                return defer.promise;

            }
        };
    });

    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/login', {
        templateUrl: 'views/login.html',
        controller: 'LoginCtrl',
        controllerAs: 'login'
      })
      .otherwise({
        redirectTo: '/'
      });


    //$mdThemingProvider.theme('default')
    //.primaryPalette('red')
    //.dark();
    //$mdThemingProvider.setDefaultTheme('docs-dark');

  })
  .factory("Files", function($resource) {
  return $resource("/api/files");
  })
  .factory("User", function($resource) {
  return $resource("/api/user");
  })
  .factory("SourceActive", function($resource) {
  return $resource("/api/source/:id/active");
  })
  .factory("SourceDisable", function($resource) {
  return $resource("/api/source/:id/disable");
  });

  app.directive('helpButton', function(){
    return function(scope, element, attrs){
        attrs.$observe('helpButton', function(value) {
            element.css({
                'background-image': 'url(' + value +')',
                'background-size' : 'cover'
            });
        });
    };
});

