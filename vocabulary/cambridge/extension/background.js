chrome.runtime.onInstalled.addListener(function() {
  chrome.contextMenus.create({
      id: "sampleContextMenu",
      title: "Save to Notion Database",
      contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
  if (info.menuItemId === "sampleContextMenu") {
      console.log("Sample context menu item clicked");
      console.log("Selected text: " + info.selectionText);
      console.log("Current URL: " + tab.url);
      // 构造要发送到服务器的数据
      const data = { text: info.selectionText, url: tab.url };
      console.log("data="+data)
      // 发送POST请求到Django视图函数
      fetch('http://localhost:8000/cambridge/extension', {
          method: 'POST', 
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('HTTP error ' + response.status);
          }
          return response.json();
      })
      .then(data => {
        if (data.status === 'Update Sucess') {
            console.log('Success:', data);
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'success.png', // replace with your success icon
                title: 'Success',
                message: 'Successfully added to the notes.'
            });
        } else {
            console.error('Error:', data);
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'fail.png', // replace with your error icon
                title: 'Error',
                message: 'Failed to add to the notes.'
            });
        }
    })
      .catch((error) => {
          console.error('Error:', error);
          chrome.notifications.create({
              type: 'basic',
              iconUrl: 'fail.png', // replace with your error icon
              title: 'Error',
              message: 'Failed to add to the notes.'
          });
      });
  }
});
