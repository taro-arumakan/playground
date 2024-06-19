function generateDownloadUrls() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();

  var output = [];
  output.push(['Product', 'Image Name', 'Download URL']);

  // Adjust these indices according to your sheet
  var linkColumnIndex = 14; // Google Drive Link column (O)
  var productColumnIndex = 8; // SKU column (I)

  for (var i = 5; i < data.length; i++) { // Start from row 3 to skip header
    var product = data[i][productColumnIndex];
    var folderUrl = data[i][linkColumnIndex];
    Logger.log("folderUrl: " + folderUrl);
    var folderId = getFolderIdFromUrl(folderUrl);
    Logger.log("folderId: " + folderId);
    if (folderId) {
      var urls = getFolderImageUrls(folderId);
      for (var j = 0; j < urls.length; j++) {
        output.push([product, urls[j].name, urls[j].url]);
      }
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

  // sorts the files array by file names alphabetically
  files = files.sort(function (a, b) {
    var aName = a.getName().toUpperCase();
    var bName = b.getName().toUpperCase();
    return aName.localeCompare(bName);
  });

  var urls = [];

  for (let file of files) {
    if (file.getMimeType().startsWith('image/')) {
      urls.push({ name: file.getName(), url: file.getDownloadUrl() });
    }
  }

  return urls;
}