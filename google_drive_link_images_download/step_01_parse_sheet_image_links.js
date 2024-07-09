function generateDownloadUrls() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();

  var output = [];
  output.push(['Product', 'Image Name', 'Download URL', 'Skipped']);

  // Adjust these indices according to your sheet
  var linkColumnIndex = 14; // Google Drive Link column (O)
  var productColumnIndex = 8; // SKU column (I)

  var processedFolders = new Set();
  var skippedSKUs = [];

  for (var i = 4; i < data.length; i++) { // Start from row 4 to skip header
    var product = data[i][productColumnIndex];
    Logger.log(`processing: ${product}`);
    var folderUrl = data[i][linkColumnIndex];
    var folderId = getFolderIdFromUrl(folderUrl);
    Logger.log(`folderId: ${folderId}`);
    if (folderId) {
      if (processedFolders.has(folderId)) {
        Logger.log(`Skipping already processed folder ${folderId} for ${product}`);
        skippedSKUs.push(product);
        output.push([product, '', '', 'Yes']);
        continue;
      }
      var urls = getFolderImageUrls(folderId);
      for (const url of urls) {
        var originalName = url.name;
        Logger.log(`  processing: ${originalName}`);
        var match = originalName.match(/_(\d+)(\..*)$/);
        var newName;
        if (match) {
          var sequenceNumber = parseInt(match[1], 10);
          var paddedNumber = ('0' + sequenceNumber).slice(-2);
          newName = originalName.replace(/_(\d+)(\..*)$/, `_${paddedNumber}$2`);
        } else {
          Logger.log(`  !!! file name pattern did not match: ${originalName}`);
          newName = originalName; // Keep the original name if no match
        }
        Logger.log(`  file name is: ${newName}`);
        output.push([product, newName, url.url, 'No']);
      }
      processedFolders.add(folderId);
    }
  }

  var csvContent = '';
  output.forEach(function (rowArray) {
    let row = rowArray.join(",");
    csvContent += row + "\r\n";
  });

  var blob = Utilities.newBlob(csvContent, 'text/csv', 'downloadUrls.csv');
  var file = DriveApp.createFile(blob);
  Logger.log('Download URLs file created: ' + file.getUrl());
}

function getFolderIdFromUrl(url) {
  var match = url.match(/[-\w]{25,}/);
  return match ? match[0] : null;
}

function getFolderImageUrls(folderId) {
  var folder = DriveApp.getFolderById(folderId);
  var files_itr = folder.getFiles();
  var files = [];
  while (files_itr.hasNext()) {
    var file = files_itr.next();
    files.push(file);
  }

  // Sorts the files array by the numeric part of the file names after the underscore
  files = files.sort(function (a, b) {
    var aName = a.getName();
    var bName = b.getName();
    var aMatch = aName.match(/_(\d+)(\..*)$/);
    var bMatch = bName.match(/_(\d+)(\..*)$/);
    var aNumber = aMatch ? parseInt(aMatch[1], 10) : 0;
    var bNumber = bMatch ? parseInt(bMatch[1], 10) : 0;
    return aNumber - bNumber;
  });

  var urls = [];

  for (let file of files) {
    if (file.getMimeType().startsWith('image/')) {
      urls.push({ name: file.getName(), url: file.getDownloadUrl() });
    }
  }

  return urls;
}