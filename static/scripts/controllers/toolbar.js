'use strict';

/**
 * @ngdoc function
 * @name dataportalApp.controller:ToolbarCtrl
 * @description
 * # ToolbarCtrl
 * Controller of the dataportalApp
 */
angular.module('dataportalApp')
  .controller('ToolbarCtrl', function ($location, $http, $scope, $mdSidenav) {

    $scope.logout = function() {
      window.location.href = 'api/logout';
    };

    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
