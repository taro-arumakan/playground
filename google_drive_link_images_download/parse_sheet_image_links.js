function generateProductionDownloadUrls() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();

  var output = [];
  output.push(['Product', 'Image Name', 'Download URL', 'Skipped']);

  // Adjust these indices according to your sheet
  var linkColumnIndex = 14; // Links are in column O
  var productColumnIndex = 8; // SKU in column I

  // ID of the production version folder
  var productionFolderId = '1E10XkX6148vo2DpMNrUN1H7G-DLgAG9t'; // Update with your actual production folder ID
  var productionFolder = DriveApp.getFolderById(productionFolderId);
  var productionFolders = productionFolder.getFolders();

  var productionFoldersMap = {};
  while (productionFolders.hasNext()) {
    var folder = productionFolders.next();
    productionFoldersMap[folder.getName()] = folder.getId();
  }

  var processedFolders = new Set();
  var skippedSKUs = [];

  for (var i = 1; i < data.length; i++) { // Start from row 2 to skip header
    var product = data[i][productColumnIndex];
    var folderUrl = data[i][linkColumnIndex];
    var folderId = getFolderIdFromUrl(folderUrl);

    Logger.log(`processing ${product}`);
    if (folderId) {
      var folderName = DriveApp.getFolderById(folderId).getName();
      if (processedFolders.has(folderName)) {
        Logger.log('Skipping already processed folder: ' + folderName);
        skippedSKUs.push(product);
        output.push([product, '', '', 'Yes']);
        continue;
      }

      if (productionFoldersMap[folderName]) {
        var productionFolderId = productionFoldersMap[folderName];
        var urls = getFolderImageUrls(productionFolderId);
        for (var j = 0; j < urls.length; j++) {
          output.push([product, urls[j].name, urls[j].url, 'No']);
        }
        processedFolders.add(folderName);
      } else {
        Logger.log('No matching production folder found for: ' + folderName);
        output.push([product, '', '', 'No']);
      }
    }
  }

  var csvContent = '';
  output.forEach(function (rowArray) {
    let row = rowArray.join(",");
    csvContent += row + "\r\n";
  });

  var blob = Utilities.newBlob(csvContent, 'text/csv', 'productionDownloadUrls.csv');
  var file = DriveApp.createFile(blob);
  Logger.log('Production download URLs file created: ' + file.getUrl());
}

function getFolderIdFromUrl(url) {
  var match = url.match(/[-\w]{25,}/);
  return match ? match[0] : null;
}

function getFolderImageUrls(folderId) {
  var folder = DriveApp.getFolderById(folderId);
  var files = folder.getFiles();
  var urls = [];

  while (files.hasNext()) {
    var file = files.next();
    if (file.getMimeType().startsWith('image/')) {
      urls.push({ name: file.getName(), url: file.getDownloadUrl() });
    }
  }

  return urls;
}
