'use strict';

/**
 * @ngdoc function
 * @name dataportalApp.controller:DevicesCtrl
 * @description
 * # DevicesCtrl
 * Controller of the dataportalApp
 */
angular.module('dataportalApp')
  .controller('DevicesCtrl', function ($scope, $mdToast, SourceActive, SourceDisable) {

    SourceActive.get({ id: "w2ewithings" }, function(data) {
     $scope.w2ewithings = {}
     $scope.w2ewithings.active = (data.active === "true")
    })

    SourceActive.get({ id: "w2emoves" }, function(data) {
     $scope.w2emoves = {}
     $scope.w2emoves.active = (data.active === "true")
    })

    $scope.linkDevice = function (device) {
        if ($scope[device].active) {
        SourceDisable.delete({ id: device }, function() {
        $scope[device].active = false
        })
        } else {
        window.location.href = 'link/' + device;
        }
    };

    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

  });
