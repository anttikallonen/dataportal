'use strict';

/**
 * @ngdoc function
 * @name dataportalApp.controller:FilesCtrl
 * @description
 * # FilesCtrl
 * Controller of the dataportalApp
 */
angular.module('dataportalApp')
  .controller("FileCtrl", function($timeout, $scope, $mdDialog, Files, Upload) {

    $scope.files = Files.query(function() {});
    $scope.pendingFiles = [];

    // upload on file select or drop
    $scope.upload = function (file) {
      if (file != null) {
        // Insert dummy file here
        file.complete = 0
        $scope.pendingFiles.push(file)

        Upload.upload({
          url: 'api/files',
          headers: {'Content-Type': 'multipart/form-data' },
          data: {file: file}
        }).progress(function (evt) {
          var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
          file.complete = progressPercentage
        }).success(function (data, status, headers, config) {
          $timeout(function() {
            // remove dummy file
            var index = $scope.pendingFiles.indexOf(file);
            $scope.pendingFiles.splice(index, 1);
            $scope.files = Files.query(function() {});
            console.log('Success ' + config.data.file.name + ' uploaded.');
          });
        }).error(function(data, status, headers, config) {
          console.log("Error uploading files due to: " + JSON.stringify(data));
        });
      };
    };

    var originatorEv;
    $scope.openMenu = function($mdOpenMenu, ev) {
      originatorEv = ev;
      $mdOpenMenu(ev);
    };

    $scope.removeItem = function(fileid) {
      $scope.files.forEach(function(f, index) {
        if (f.id == fileid) {
          Files.delete({ id: fileid }, function() {
            $scope.files.splice(index, 1);
          });
        }
      });
    };

  });
