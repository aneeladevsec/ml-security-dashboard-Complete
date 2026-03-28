// Background service worker
chrome.runtime.onInstalled.addListener(() => {
  console.log('🚀 AI Security Extension installed');
  
  // Initialize storage
  chrome.storage.local.set({ scans: [] });
});

// Listen for tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    // Could trigger automatic analysis here
    console.log('Page loaded:', tab.url);
  }
});

// Handle messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getScans') {
    chrome.storage.local.get(['scans'], (result) => {
      sendResponse(result.scans || []);
    });
    return true; // Keep channel open for async
  }
});
