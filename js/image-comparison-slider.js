(function () {
  /**
   * Format file size to human readable string (KB / MB)
   */
  function formatSize(bytes) {
    if (bytes === 0) return '0 KB';
    const k = 1024;
    const dm = 1;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  /**
   * Helper to resolve original and converted images from the page state
   */
  function getPageState() {
    if (typeof state !== 'undefined') {
      const originalFile = state.uploadedFiles && state.uploadedFiles[0];
      const convertedImg = (state.compressedImages && state.compressedImages[0]) || 
                           (state.convertedImages && state.convertedImages[0]);
      if (originalFile && convertedImg) {
        return {
          originalFile: originalFile,
          convertedUrl: convertedImg.url,
          originalSize: originalFile.size,
          convertedSize: convertedImg.size
        };
      }
    }
    
    // Fallback: try using DOM elements
    const fileInput = document.getElementById('fileInput');
    const downloadSection = document.getElementById('downloadSection');
    if (fileInput && fileInput.files && fileInput.files[0] && downloadSection) {
      const img = downloadSection.querySelector('img');
      if (img && img.src) {
        return {
          originalFile: fileInput.files[0],
          convertedUrl: img.src,
          originalSize: fileInput.files[0].size,
          convertedSize: 0
        };
      }
    }
    return null;
  }

  /**
   * Initialize or update the Before/After Image Comparison Slider
   */
  window.initComparisonSlider = async function (originalSource, compressedSource, originalBytes, compressedBytes) {
    const slider = document.getElementById('comparisonSlider');
    if (!slider) return;

    const imgOriginal = slider.querySelector('.img-original');
    const imgCompressed = slider.querySelector('.img-compressed');
    const container = slider.querySelector('.slider-container');
    const skeleton = slider.querySelector('.slider-skeleton');
    const aspectHolder = slider.querySelector('.slider-aspect-ratio-holder');
    
    const sizeOrigSpan = slider.querySelector('.size-orig');
    const sizeConvSpan = slider.querySelector('.size-conv');
    const sizeDiffSpan = slider.querySelector('.size-diff');

    if (!imgOriginal || !imgCompressed || !container || !skeleton || !aspectHolder) return;

    // Reset UI state
    slider.style.display = 'block';
    skeleton.style.display = 'block';
    container.style.opacity = '0';

    // Release old URLs if they were generated locally to prevent memory leaks
    if (imgOriginal._localUrl) {
      URL.revokeObjectURL(imgOriginal._localUrl);
      imgOriginal._localUrl = null;
    }
    if (imgCompressed._localUrl) {
      URL.revokeObjectURL(imgCompressed._localUrl);
      imgCompressed._localUrl = null;
    }

    // Resolve original source and handle RAW format conversions
    let origUrl = originalSource;
    let convUrl = compressedSource;

    if (originalSource instanceof Blob || originalSource instanceof File) {
      const isRaw = originalSource.name && /\.(cr2|cr3|nef|arw|dng|raw|raf|rw2|orf|pef)$/i.test(originalSource.name);
      if (isRaw && typeof convertRawToJpgWithVips === 'function') {
        try {
          // Generate a high-quality JPG blob as the comparison base for RAW formats
          const highQualBlob = await convertRawToJpgWithVips(originalSource, 95);
          origUrl = URL.createObjectURL(highQualBlob);
          imgOriginal._localUrl = origUrl;
        } catch (e) {
          console.error("Failed to generate RAW preview comparison", e);
          origUrl = compressedSource; // Fallback to converted image if raw preview fails
        }
      } else {
        origUrl = URL.createObjectURL(originalSource);
        imgOriginal._localUrl = origUrl;
      }
    }

    if (compressedSource instanceof Blob || compressedSource instanceof File) {
      convUrl = URL.createObjectURL(compressedSource);
      imgCompressed._localUrl = convUrl;
    }

    // Update sizes and percentages
    let finalConvBytes = compressedBytes;
    if (!finalConvBytes && convUrl.startsWith('blob:')) {
      try {
        const response = await fetch(convUrl);
        const blob = await response.blob();
        finalConvBytes = blob.size;
      } catch (err) {
        console.error("Failed to fetch blob size", err);
      }
    }

    if (originalBytes && finalConvBytes) {
      if (sizeOrigSpan) sizeOrigSpan.textContent = formatSize(originalBytes);
      if (sizeConvSpan) sizeConvSpan.textContent = formatSize(finalConvBytes);
      if (sizeDiffSpan) {
        const diffPercent = ((originalBytes - finalConvBytes) / originalBytes * 100).toFixed(1);
        sizeDiffSpan.textContent = `-${diffPercent}%`;
      }
    }

    // Wait for both images to load to align aspect ratio and avoid layout shifts
    let imagesLoaded = 0;
    function checkImagesLoaded() {
      imagesLoaded++;
      if (imagesLoaded === 2) {
        // Read natural aspect ratio of the image
        const w = imgOriginal.naturalWidth || 800;
        const h = imgOriginal.naturalHeight || 450;
        aspectHolder.style.aspectRatio = `${w} / ${h}`;
        
        // Hide skeleton and reveal slider container
        skeleton.style.display = 'none';
        container.style.opacity = '1';
        
        // Update dimensions of compressed image to align perfectly
        const holderWidth = aspectHolder.clientWidth;
        imgCompressed.style.width = holderWidth + 'px';
      }
    }

    imgOriginal.onload = checkImagesLoaded;
    imgCompressed.onload = checkImagesLoaded;

    imgOriginal.src = origUrl;
    imgCompressed.src = convUrl;
  };

  /**
   * Automatic observer to initialize comparison slider on conversion finish
   */
  document.addEventListener('DOMContentLoaded', function () {
    const downloadSection = document.getElementById('downloadSection');
    const aspectHolder = document.querySelector('.slider-aspect-ratio-holder');
    const overlayWrapper = document.querySelector('.img-compressed-wrapper');
    const imgCompressed = document.querySelector('.img-compressed');
    const handle = document.querySelector('.slider-handle');

    if (!downloadSection || !aspectHolder || !overlayWrapper || !imgCompressed || !handle) return;

    let isSliding = false;
    let lastUrl = '';

    // Align compressed image width on window resize
    window.addEventListener('resize', function () {
      if (imgCompressed.style.opacity !== '0') {
        imgCompressed.style.width = aspectHolder.clientWidth + 'px';
      }
    });

    // Slider mouse/touch movement logic
    function startSliding(e) {
      e.preventDefault();
      isSliding = true;
    }

    function stopSliding() {
      isSliding = false;
    }

    function slideMove(e) {
      if (!isSliding) return;
      const rect = aspectHolder.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      let offsetX = clientX - rect.left;
      
      if (offsetX < 0) offsetX = 0;
      if (offsetX > rect.width) offsetX = rect.width;
      
      const percentage = (offsetX / rect.width) * 100;
      overlayWrapper.style.width = (100 - percentage) + '%';
      handle.style.left = percentage + '%';
    }

    handle.addEventListener('mousedown', startSliding);
    window.addEventListener('mouseup', stopSliding);
    window.addEventListener('mousemove', slideMove);

    handle.addEventListener('touchstart', startSliding, { passive: true });
    window.addEventListener('touchend', stopSliding);
    window.addEventListener('touchmove', slideMove, { passive: true });

    // Observer to detect when downloadSection is displayed
    const observer = new MutationObserver(function () {
      const isVisible = downloadSection.style.display === 'block';
      const slider = document.getElementById('comparisonSlider');
      
      if (isVisible) {
        // Wait briefly for download items to render in DOM
        setTimeout(function () {
          const pageState = getPageState();
          if (pageState && pageState.convertedUrl !== lastUrl) {
            lastUrl = pageState.convertedUrl;
            // Reset overlay width to center
            overlayWrapper.style.width = '50%';
            handle.style.left = '50%';
            // Initialize slider
            window.initComparisonSlider(
              pageState.originalFile,
              pageState.convertedUrl,
              pageState.originalSize,
              pageState.convertedSize
            );
          }
        }, 80);
      } else {
        if (slider) {
          slider.style.display = 'none';
          lastUrl = '';
        }
      }
    });

    observer.observe(downloadSection, { attributes: true, attributeFilter: ['style'] });
  });
})();
