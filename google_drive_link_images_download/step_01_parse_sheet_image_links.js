function generateDownloadUrls() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();

  var output = [];
  output.push(['Product', 'Image Name', 'Download URL', 'Skipped']);

  // Adjust these indices according to your sheet
  var linkColumnIndex = 13; // Google Drive Link column (N)
  var productColumnIndex = 5; // SKU column (F)
  var startRow = 3; // skip headers - zero base

  var processedFolders = new Set();
  var skippedSKUs = [];

  for (var i = startRow; i < data.length; i++) {
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
        Logger.log(`  file name is: ${url.name}`);
        output.push([product, url.name, url.url, 'No']);
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

  // Sort the files using natural order (considering numeric parts)
  files.sort(function (a, b) {
    return naturalCompare(a.getName(), b.getName());
  });

  var urls = [];

  for (let file of files) {
    if (file.getMimeType().startsWith('image/')) {
      urls.push({ name: file.getName(), url: file.getDownloadUrl() });
    }
  }

  return urls;
}

// Function to compare two strings in a natural order (considering numeric parts)
function naturalCompare(a, b) {
  return a.toLowerCase().localeCompare(b.toLowerCase(), undefined, { numeric: true, sensitivity: 'base' });
}