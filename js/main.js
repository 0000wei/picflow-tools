// PicFlow - Main JavaScript File

// Global state
const state = {
    uploadedFiles: [],
    processedImages: [],
    originalDimensions: []
};

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const selectBtn = document.getElementById('selectBtn');
const processingArea = document.getElementById('processingArea');
const previewGrid = document.getElementById('previewGrid');
const downloadSection = document.getElementById('downloadSection');
const downloadGrid = document.getElementById('downloadGrid');
const processBtn = document.getElementById('processBtn');
const resetBtn = document.getElementById('resetBtn');
const qualitySlider = document.getElementById('qualitySlider');
const qualityValue = document.getElementById('qualityValue');
const widthInput = document.getElementById('widthInput');
const heightInput = document.getElementById('heightInput');
const maintainAspect = document.getElementById('maintainAspect');
const downloadAllBtn = document.getElementById('downloadAllBtn');
const startOverBtn = document.getElementById('startOverBtn');

// Initialize event listeners
function init() {
    // Upload area events
    selectBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', (e) => {
        if (e.target === uploadArea || e.target.closest('.upload-icon') || e.target.closest('.upload-text')) {
            fileInput.click();
        }
    });

    // Process button events
    processBtn.addEventListener('click', processImages);
    resetBtn.addEventListener('click', resetSelection);
    downloadAllBtn.addEventListener('click', downloadAll);
    startOverBtn.addEventListener('click', startOver);

    // Quality slider event
    qualitySlider.addEventListener('input', (e) => {
        qualityValue.textContent = e.target.value;
    });

    // Dimension input events
    widthInput.addEventListener('input', handleWidthChange);
    heightInput.addEventListener('input', handleHeightChange);
}

// File selection handler
function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

// Drag and drop handler
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');

    const files = Array.from(e.dataTransfer.files);
    const imageFiles = files.filter(file => file.type.startsWith('image/'));
    addFiles(imageFiles);
}

// Add files to state
function addFiles(files) {
    if (files.length === 0) {
        alert('Please select valid image files');
        return;
    }

    state.uploadedFiles = files;
    state.originalDimensions = [];

    Promise.all(files.map(file => loadImage(file)))
        .then(images => {
            displayPreviews(images);
            uploadArea.style.display = 'none';
            processingArea.style.display = 'block';
        })
        .catch(error => {
            console.error('Failed to load images:', error);
            alert('Failed to load images, please try again');
        });
}

// Load image
function loadImage(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                state.originalDimensions.push({
                    width: img.width,
                    height: img.height
                });
                resolve({ img, file, src: e.target.result });
            };
            img.onerror = reject;
            img.src = e.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Display previews
function displayPreviews(images) {
    previewGrid.innerHTML = '';

    images.forEach(({ img, file, src }, index) => {
        const div = document.createElement('div');
        div.className = 'preview-item';
        div.innerHTML = `
            <img src="${src}" alt="${file.name}">
            <div class="file-info">
                <strong>${file.name}</strong><br>
                ${img.width} × ${img.height}px<br>
                ${formatFileSize(file.size)}
            </div>
        `;
        previewGrid.appendChild(div);
    });

    // Set initial dimensions from the first image
    if (state.originalDimensions.length > 0) {
        const firstDim = state.originalDimensions[0];
        widthInput.placeholder = firstDim.width;
        heightInput.placeholder = firstDim.height;
    }
}

// Process images
async function processImages() {
    if (state.uploadedFiles.length === 0) {
        alert('Please select images first');
        return;
    }

    const format = document.querySelector('input[name="format"]:checked')?.value || 'jpeg';
    const quality = parseInt(qualitySlider.value) / 100;
    const width = parseInt(widthInput.value);
    const height = parseInt(heightInput.value);

    state.processedImages = [];

    for (let i = 0; i < state.uploadedFiles.length; i++) {
        try {
            const result = await processImage(
                state.uploadedFiles[i],
                state.originalDimensions[i],
                { format, quality, width, height }
            );
            state.processedImages.push(result);
        } catch (error) {
            console.error('Failed to process image:', error);
            alert(`Failed to process ${state.uploadedFiles[i].name}`);
        }
    }

    displayDownloads();
}

// Process single image
function processImage(file, originalDim, options) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');

                // Calculate new dimensions
                let newWidth = originalDim.width;
                let newHeight = originalDim.height;

                if (options.width && options.height) {
                    newWidth = options.width;
                    newHeight = options.height;
                } else if (options.width) {
                    newWidth = options.width;
                    newHeight = Math.round((originalDim.height * options.width) / originalDim.width);
                } else if (options.height) {
                    newHeight = options.height;
                    newWidth = Math.round((originalDim.width * options.height) / originalDim.height);
                }

                canvas.width = newWidth;
                canvas.height = newHeight;

                // Draw image
                ctx.drawImage(img, 0, 0, newWidth, newHeight);

                // Convert format
                const mimeTypes = {
                    'jpeg': 'image/jpeg',
                    'png': 'image/png',
                    'webp': 'image/webp'
                };

                canvas.toBlob((blob) => {
                    if (blob) {
                        const url = URL.createObjectURL(blob);
                        resolve({
                            url,
                            blob,
                            name: file.name.replace(/\.[^/.]+$/, '') + '.' + (options.format === 'jpeg' ? 'jpg' : options.format),
                            size: blob.size,
                            width: newWidth,
                            height: newHeight
                        });
                    } else {
                        reject(new Error('Canvas conversion failed'));
                    }
                }, mimeTypes[options.format], options.quality);
            };
            img.onerror = reject;
            img.src = e.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Display download area
function displayDownloads() {
    processingArea.style.display = 'none';
    downloadSection.style.display = 'block';

    downloadGrid.innerHTML = '';

    state.processedImages.forEach((image, index) => {
        const div = document.createElement('div');
        div.className = 'download-item';
        div.innerHTML = `
            <img src="${image.url}" alt="${image.name}">
            <h4>${image.name}</h4>
            <p>${image.width} × ${image.height}px | ${formatFileSize(image.size)}</p>
            <button class="btn-primary" onclick="downloadImage(${index})">Download</button>
        `;
        downloadGrid.appendChild(div);
    });
}

// Download single image
window.downloadImage = function(index) {
    const image = state.processedImages[index];
    const a = document.createElement('a');
    a.href = image.url;
    a.download = image.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
};

// Download all images
function downloadAll() {
    state.processedImages.forEach((image, index) => {
        setTimeout(() => {
            window.downloadImage(index);
        }, index * 500); // 500ms interval to prevent browser blocking multiple downloads
    });
}

// Reset selection
function resetSelection() {
    state.uploadedFiles = [];
    state.processedImages = [];
    state.originalDimensions = [];

    fileInput.value = '';
    widthInput.value = '';
    heightInput.value = '';
    qualitySlider.value = 85;
    qualityValue.textContent = '85';

    document.querySelectorAll('input[name="format"]')[0].checked = true;

    processingArea.style.display = 'none';
    downloadSection.style.display = 'none';
    uploadArea.style.display = 'block';
}

// Start new processing
function startOver() {
    resetSelection();
}

// Width change handler
function handleWidthChange() {
    if (!maintainAspect.checked || state.originalDimensions.length === 0) return;

    const width = parseInt(widthInput.value);
    if (!width) return;

    const original = state.originalDimensions[0];
    const aspectRatio = original.height / original.width;
    const newHeight = Math.round(width * aspectRatio);
    heightInput.value = newHeight;
}

// Height change handler
function handleHeightChange() {
    if (!maintainAspect.checked || state.originalDimensions.length === 0) return;

    const height = parseInt(heightInput.value);
    if (!height) return;

    const original = state.originalDimensions[0];
    const aspectRatio = original.width / original.height;
    const newWidth = Math.round(height * aspectRatio);
    widthInput.value = newWidth;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Initialize
init();
