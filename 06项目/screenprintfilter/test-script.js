// Test script for ScreenPrintFilter functionality
// Run this in browser console when localhost:33345 is open

console.log("=== ScreenPrintFilter Test Script ===\n");

// Test 5: Undo/Redo
function testUndoRedo() {
    console.log("Test 5: Undo/Redo Functionality");
    console.log("1. Testing Ctrl+Z shortcut...");

    // Simulate Ctrl+Z
    const event = new KeyboardEvent('keydown', {
        key: 'z',
        ctrlKey: true,
        shiftKey: false
    });
    document.dispatchEvent(event);
    console.log("   Ctrl+Z dispatched");

    // Check undo button state
    const undoBtn = document.getElementById('undoBtn');
    console.log("   Undo button disabled: " + undoBtn.disabled);

    console.log("2. Testing Ctrl+Shift+Z shortcut...");
    const redoEvent = new KeyboardEvent('keydown', {
        key: 'z',
        ctrlKey: true,
        shiftKey: true
    });
    document.dispatchEvent(redoEvent);
    console.log("   Ctrl+Shift+Z dispatched");

    const redoBtn = document.getElementById('redoBtn');
    console.log("   Redo button disabled: " + redoBtn.disabled);

    console.log("3. Testing slider change triggers undo...");
    const dotSizeSlider = document.getElementById('dotSize');
    const initialValue = dotSizeSlider.value;
    dotSizeSlider.value = parseInt(initialValue) + 2;
    dotSizeSlider.dispatchEvent(new Event('input', { bubbles: true }));
    dotSizeSlider.dispatchEvent(new Event('change', { bubbles: true }));
    console.log("   Slider changed from " + initialValue + " to " + dotSizeSlider.value);

    console.log("   Undo button disabled after slider change: " + undoBtn.disabled);
    console.log("✅ Test 5 Complete\n");
}

// Test 7: Download with custom size
function testDownloadCustomSize() {
    console.log("Test 7: Download with Custom Size");

    const useOriginalSizeCheckbox = document.getElementById('useOriginalSize');
    const outputWidthInput = document.getElementById('outputWidth');
    const outputHeightInput = document.getElementById('outputHeight');

    console.log("1. Switching to custom size...");
    useOriginalSizeCheckbox.checked = false;
    useOriginalSizeCheckbox.dispatchEvent(new Event('change', { bubbles: true }));

    console.log("   Use Original Size: " + useOriginalSizeCheckbox.checked);
    console.log("   Width input disabled: " + outputWidthInput.disabled);
    console.log("   Height input disabled: " + outputHeightInput.disabled);

    console.log("2. Setting custom dimensions...");
    outputWidthInput.value = 500;
    outputHeightInput.value = 500;
    outputWidthInput.dispatchEvent(new Event('input', { bubbles: true }));
    outputHeightInput.dispatchEvent(new Event('input', { bubbles: true }));

    console.log("   Width: " + outputWidthInput.value);
    console.log("   Height: " + outputHeightInput.value);

    const canvas = document.getElementById('mainCanvas');
    console.log("   Canvas size: " + canvas.width + "x" + canvas.height);

    console.log("3. Testing download button...");
    const downloadBtn = document.getElementById('downloadBtn');
    console.log("   Download button disabled: " + downloadBtn.disabled);

    console.log("✅ Test 7 Complete\n");
}

// Test 11: Output Size switching
function testOutputSizeSwitching() {
    console.log("Test 11: Output Size Switching");

    const useOriginalSizeCheckbox = document.getElementById('useOriginalSize');
    const outputWidthInput = document.getElementById('outputWidth');
    const outputHeightInput = document.getElementById('outputHeight');
    const canvas = document.getElementById('mainCanvas');

    console.log("1. Initial state (original size)...");
    console.log("   Use Original Size: " + useOriginalSizeCheckbox.checked);
    console.log("   Canvas size: " + canvas.width + "x" + canvas.height);

    console.log("2. Switching to custom size...");
    useOriginalSizeCheckbox.checked = false;
    useOriginalSizeCheckbox.dispatchEvent(new Event('change', { bubbles: true }));

    console.log("   Canvas size after switching: " + canvas.width + "x" + canvas.height);

    console.log("3. Switching back to original size...");
    useOriginalSizeCheckbox.checked = true;
    useOriginalSizeCheckbox.dispatchEvent(new Event('change', { bubbles: true }));

    console.log("   Canvas size after switching back: " + canvas.width + "x" + canvas.height);

    console.log("✅ Test 11 Complete\n");
}

// Test 12: AI Friendly files (check via fetch)
async function testAIFriendlyFiles() {
    console.log("Test 12: AI Friendly Files");

    const files = [
        '/llms.txt',
        '/.well-known/llms.txt',
        '/.well-known/ai-plugin.json'
    ];

    for (const file of files) {
        try {
            const response = await fetch(file);
            console.log(`   ${file}: ${response.status} ${response.statusText}`);
        } catch (error) {
            console.log(`   ${file}: ERROR - ${error.message}`);
        }
    }

    console.log("✅ Test 12 Complete\n");
}

// Run all tests
function runAllTests() {
    console.log("Starting all tests...\n");
    testUndoRedo();
    testDownloadCustomSize();
    testOutputSizeSwitching();
    testAIFriendlyFiles();
    console.log("=== All tests completed ===");
}

// Instructions
console.log("Available test functions:");
console.log("  testUndoRedo() - Test undo/redo functionality");
console.log("  testDownloadCustomSize() - Test custom size download");
console.log("  testOutputSizeSwitching() - Test output size switching");
console.log("  testAIFriendlyFiles() - Test AI friendly files");
console.log("  runAllTests() - Run all tests");
console.log("\nNote: Make sure an image is loaded before running tests 5, 7, and 11");