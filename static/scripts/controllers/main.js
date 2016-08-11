'use strict';

/**
 * @ngdoc function
 * @name dataportalApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the dataportalApp
 */
angular.module('dataportalApp')
  .controller('MainCtrl', function ($scope, $rootScope, $mdDialog, Files, User) {

    $rootScope.user = User.get(function() {
    console.log("User is");
    console.log($rootScope.user);
    });

    $scope.openPage = function (pageUrl) {
      window.location.href = pageUrl;
    };

    $rootScope.showHelpDialog = function(ev, text) {
    // Appending dialog to document.body to cover sidenav in docs app
    // Modal dialogs should fully cover application
    // to prevent interaction outside of dialog
    $mdDialog.show(
      $mdDialog.alert()
        .parent(angular.element(document.querySelector('#popupContainer')))
        .clickOutsideToClose(true)
        .title('Apua')
        .textContent(text)
        .ariaLabel('Apua')
        .ok('OK')
        .targetEvent(ev)
    );
  };


    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });

