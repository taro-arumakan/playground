function listFolderURLs() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var startRow = 5; // The row where product names start
  var productNameColumn = 6; // Column F
  var colorColumn = 7; // Column G
  var sizeColumn = 8; // Column H
  var folderURLColumn = 24; // Assuming you want to put URLs in the second column (B)

  var driveFolder = DriveApp.getFolderById('19LBJhNj-00634bgL-CAOHCVPMgC6OnOR'); // Replace with your Google Drive folder ID
  var folders = driveFolder.getFolders();

  var folderMap = {};

  while (folders.hasNext()) {
    var folder = folders.next();
    folderMap[folder.getName().toLowerCase()] = folder.getUrl();
  }

  var range = sheet.getRange(startRow, productNameColumn, sheet.getLastRow() - startRow + 1, 3); // Getting columns F, G, H
  var values = range.getValues();

  for (var i = 0; i < values.length; i++) {
    var productName = values[i][0].toString().toLowerCase();
    var color = values[i][1].toString().toLowerCase();
    var size = values[i][2].toString().toLowerCase();

    var fullMatch = productName + ' ' + color + ' ' + size;
    var partialMatch = productName + ' ' + color;

    var found = false;
    Logger.log(`searching ${productName}, ${color}, ${size}`);
    if (folderMap[fullMatch]) {
      sheet.getRange(startRow + i, folderURLColumn).setValue(folderMap[fullMatch]);
      Logger.log('full match');
      found = true;
    } else if (folderMap[partialMatch]) {
      sheet.getRange(startRow + i, folderURLColumn).setValue(folderMap[partialMatch]);
      Logger.log('color match');
      found = true;
    } else {
      for (var folderName in folderMap) {
        if (folderName.startsWith(productName)) {
          sheet.getRange(startRow + i, folderURLColumn).setValue(folderMap[folderName]);
          Logger.log('starts with match');
          found = true;
          break;
        }
      }
    }

    if (!found) {
      sheet.getRange(startRow + i, folderURLColumn).setValue('Folder not found');
    }
  }
}