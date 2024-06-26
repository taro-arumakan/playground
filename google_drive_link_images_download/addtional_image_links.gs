function generateProductionDownloadUrls() {
  var output = [];
  output.push(['Product', 'Image Name', 'Download URL', 'Skipped']);

  var dir_map = {
    'S02739': 'https://drive.google.com/drive/folders/1XrHiWbEYV23sT1dfSIY_IGdOT936Lw6c?usp=drive_link',
    'S02740': 'https://drive.google.com/drive/folders/1Wh6Pz9u6YKiTGL6IbVOuHvtnCqYvTkBc?usp=drive_link',
    '45042': 'https://drive.google.com/drive/folders/1B9GQhHmoowKprxJfdZrg8hhk4pUtGaP9?usp=drive_link',
    '05658': 'https://drive.google.com/drive/folders/1uYU7wtmiZLTTLd3otvPgbgNyxi7kmzI-?usp=drive_link',
    'S03681': 'https://drive.google.com/drive/folders/1yCLMGp8Tj_JgN89e1loCnxRya64vOKK-',
    'S32578': 'https://drive.google.com/drive/folders/1skKg2TBIdHHVg-GCJ0ZTpkeXWMtsrUVM',
    '04419': 'https://drive.google.com/drive/folders/1BG4caKn_qplpZuxyt8-nb2SMhPCBUJ_0',
    '04420': 'https://drive.google.com/drive/folders/1aX1aT8Shb8W9V5ibVHYdv2_TbDygk2r9',
    '31281': 'https://drive.google.com/drive/folders/1_24uJc1it_ErgMkKxuhBchcKHLBLFLlo',
    '41711': 'https://drive.google.com/drive/folders/1i7aWsypbPyNIaSnzmBofpGNT-zbj7-Y_',
    'S45045': 'https://drive.google.com/drive/folders/1UT55Z1FWIO_Vc8m_cOqXs8E9HGGKIb13',
    '04441': 'https://drive.google.com/drive/folders/15oIWPiKY9xvUL4MOJHs7QEnoT7G67S9_',
    'S46847': 'https://drive.google.com/drive/folders/1v0YhztMhU-FK0EhMCof4Rvb71MXx4Czd',
    'S46848': 'https://drive.google.com/drive/folders/18wgLbXXr_8ZrD9WTKdr1UUSkZl1FnqXW',
  };

  for (const [sku, url] of Object.entries(dir_map)){
    var folderId = getFolderIdFromUrl(url);
    Logger.log(`processing ${sku}: ${folderId}`);
    var urls = getFolderImageUrls(folderId);
    for (var j = 0; j < urls.length; j++) {
      output.push([sku, urls[j].name, urls[j].url, 'No']);
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
