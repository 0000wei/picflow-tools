# Facebook Cover Safe Zone Cropper — Test Cases

Project: PicEte
Tool: resize-image-for-facebook-cover
Date: 2026-06-08
Version: Phase 1 (12/16 Tasks completed)
Test method: Automated CDP browser testing (headless Chrome 148)

---

## A. Upload (TC-1 to TC-4)

### TC-1: Upload image via click-to-browse

**Prerequisites**: Browser open at resize-image-for-facebook-cover/index.html, no image loaded yet.

**Steps**:
1. Click the upload area / "Choose File" button.
2. Select a JPG image (e.g., 1920x1080) from the file picker.
3. Wait for the image to load on canvas.

**Expected**: Image appears on canvas. Canvas dimensions are 600x314 CSS (1200x628 logical). No error messages shown. Upload area is replaced by the image with controls.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-2: Upload image via drag-and-drop

**Prerequisites**: Browser open at resize-image-for-facebook-cover/index.html, no image loaded yet.

**Steps**:
1. Drag a PNG image file from the file manager onto the upload zone.
2. Release the mouse button to drop the file.
3. Observe the canvas.

**Expected**: Image loads correctly on canvas. No file-open dialog appears. Canvas shows the dropped image.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-3: Upload image via Ctrl+V paste from clipboard

**Prerequisites**: Browser open at resize-image-for-facebook-cover/index.html. An image copied to system clipboard (e.g., screenshot).

**Steps**:
1. Press Ctrl+V while the page is focused.
2. Wait for the image to appear on canvas.

**Expected**: Image from clipboard is loaded onto canvas. No file dialog appears. Canvas shows the pasted image.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-4: Upload non-image file (error handling)

**Prerequisites**: Browser open at resize-image-for-facebook-cover/index.html.

**Steps**:
1. Attempt to drag-and-drop a .txt or .pdf file onto the upload zone.
2. Alternatively, select a non-image file via the file picker.
3. Observe the page behavior.

**Expected**: Image does not load. Either an error message is shown ("Please upload an image file") or the file is silently rejected. Canvas remains empty/unchanged. No crash.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

## B. Drag/Zoom (TC-5 to TC-8)

### TC-5: Drag image to reposition on canvas

**Prerequisites**: An image loaded on canvas (e.g., 1920x1080).

**Steps**:
1. Press and hold the left mouse button on the image.
2. Drag the mouse in any direction (e.g., left, up).
3. Release the mouse button.

**Expected**: Image pans/repositions within the canvas viewport. The canvas boundaries clip the image. No image distortion. Image remains fully renderable.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-6: Zoom in/out with mouse wheel

**Prerequisites**: An image loaded on canvas.

**Steps**:
1. Place the mouse cursor over the canvas.
2. Scroll the mouse wheel up (zoom in) — repeat a few times.
3. Scroll the mouse wheel down (zoom out) — repeat a few times.

**Expected**: Image zooms in/out centered on cursor position (or center of canvas). Zoom stays within 25%-500% range. No image distortion. Canvas viewport updates smoothly.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-7: Zoom via range slider

**Prerequisites**: An image loaded on canvas. Zoom slider control is visible.

**Steps**:
1. Drag the zoom range slider to the right (increase zoom).
2. Drag the zoom range slider to the left (decrease zoom).
3. Drag the slider to the minimum (25%) and maximum (500%) positions.

**Expected**: Image zoom level corresponds to slider position. At 100%, image is at natural size. At 25%, image is very small. At 500%, image is very large. No distortion. Slider and mouse wheel zoom are in sync.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-8: Zoom percentage display accuracy

**Prerequisites**: An image loaded on canvas.

**Steps**:
1. Note the displayed zoom percentage (default should be 100% or a sensible default).
2. Zoom in with mouse wheel until the display shows 200%.
3. Zoom out to 50%. Switch to slider and set to 100%.

**Expected**: Zoom percentage label updates in real time. Zoom level is consistent between mouse wheel and slider. At 100%, 1 logical pixel = 1 CSS pixel (or whatever the tool defines as 100%).

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

## C. Safe Zone Overlay (TC-9 to TC-11)

### TC-9: Safe zone 3x3 grid and semi-transparent overlay visual

**Prerequisites**: An image loaded on canvas. Tool is in "Safe Zone" mode (default mode).

**Steps**:
1. Observe the canvas overlay.
2. Look for a 3x3 grid dividing the canvas.
3. Look for a highlighted/semi-transparent rectangular area (560x312 logical safe zone).

**Expected**: A 3x3 grid is drawn over the canvas. A semi-transparent overlay highlights the central 560x312 safe zone area. The rest of the canvas outside the safe zone is dimmed (or vice versa). The safe zone is centered horizontally and positioned appropriately vertically.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-10: Reposition image affects safe zone content

**Prerequisites**: An image loaded on canvas. Safe Zone mode active.

**Steps**:
1. Drag the image so that the safe zone area shows a specific portion of the image (e.g., top-left corner of subject).
2. Drag the image so a different portion is inside the safe zone (e.g., bottom-right corner).
3. Observe the safe zone highlight area.

**Expected**: As the image is dragged, the content visible through the safe zone highlight changes accordingly. The safe zone overlay rectangle stays fixed on the canvas — only the image moves behind it.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-11: Safe zone dimensions are correct (560x312 logical)

**Prerequisites**: An image loaded on canvas. Safe Zone mode active. Browser DevTools open.

**Steps**:
1. Use browser DevTools to inspect the safe zone overlay element.
2. Measure its rendered dimensions in CSS pixels.
3. Convert to logical pixels (canvas is 600x314 CSS = 1200x628 logical, ratio 2:1).

**Expected**: The safe zone overlay is 280x156 CSS pixels, which maps to 560x312 logical pixels. It is centered in the canvas viewport.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

## D. Desktop Immersive Preview (TC-12 to TC-15)

### TC-12: Switch to Desktop Preview mode — visual layout

**Prerequisites**: An image loaded on canvas. Tool currently showing Safe Zone mode.

**Steps**:
1. Click the mode selector to switch to "Desktop Preview" mode.
2. Observe the canvas display.

**Expected**: The canvas changes to a 1200x312 horizontal band (600x156 CSS). A Facebook desktop-style UI overlay appears: top bar with "← Alex Johnson, Edit Cover Photo", bottom gradient bar with ~80px avatar circle, action buttons (Like/Comment/Share), and tab bar (Posts·About·Photos·More).

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-13: Desktop Preview — cover image scrolls with image position

**Prerequisites**: An image loaded. Desktop Preview mode active.

**Steps**:
1. Go back to Safe Zone mode and drag the image to a new position.
2. Switch to Desktop Preview mode.
3. Then in Desktop Preview mode, drag the image.

**Expected**: The cover image portion visible in the Desktop Preview band matches the image content positioned via Safe Zone mode. Dragging in Desktop Preview also repositions the image and the changes reflect in Safe Zone when switching back.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-14: Desktop Preview — avatar and action buttons render

**Prerequisites**: An image loaded. Desktop Preview mode active.

**Steps**:
1. Visually inspect the bottom gradient bar and avatar circle.
2. Inspect the action buttons (Like, Comment, Share).
3. Inspect the tab bar below the cover image.

**Expected**: Avatar circle appears as ~80px circle overlaid on the gradient bar. "Like", "Comment", "Share" buttons/links are visible. Tab bar shows "Posts · About · Photos · More" (or similar). All elements are positioned correctly and do not overlap the cover image area.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-15: Desktop Preview — top bar back button and edit text

**Prerequisites**: An image loaded. Desktop Preview mode active.

**Steps**:
1. Look at the top-left corner of the preview.
2. Look at the top-right area for edit text.

**Expected**: A back arrow "←" and "Alex Johnson" (or similar profile name placeholder text) appear on the top bar. "Edit Cover Photo" text or button is visible on the right side. The overall layout resembles a Facebook profile cover photo page.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

## E. Mobile Immersive Preview (TC-16 to TC-18)

### TC-16: Switch to Mobile Preview mode — visual layout

**Prerequisites**: An image loaded on canvas. Tool currently showing any mode.

**Steps**:
1. Click the mode selector to switch to "Mobile Preview" mode.
2. Observe the canvas display.

**Expected**: The canvas changes to a 560x628 vertical band (280x314 CSS). A Facebook mobile-style UI overlay appears: status bar (11:30/signal/battery), nav bar (facebook/search/notifications), bottom avatar, and action buttons. Layout resembles the Facebook iOS/Android app cover photo view.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-17: Mobile Preview — status bar and nav bar elements

**Prerequisites**: An image loaded. Mobile Preview mode active.

**Steps**:
1. Look at the top of the preview for the status bar.
2. Look below the status bar for the nav bar.
3. Look at the bottom for the avatar and action buttons.

**Expected**: Status bar shows time ("11:30" or similar), signal bars, and battery icon. Nav bar shows "facebook" logo/text, search icon, and notifications bell icon. These elements are styled for mobile (smaller, touch-friendly spacing).

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-18: Mobile Preview — scroll prevention (touch behavior base)

**Prerequisites**: An image loaded. Mobile Preview mode active.

**Steps**:
1. Use browser DevTools to emulate a mobile viewport or use touch simulation.
2. Attempt to scroll the page by touching/dragging on the canvas area.
3. Observe page scroll behavior.

**Expected**: Touching and dragging on the canvas area does NOT cause the main page to scroll. The touch event is captured by the canvas for image manipulation (drag/pan), not passed to the browser for page scrolling.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

## F. Mode Switching (TC-19 to TC-20)

### TC-19: Cycle through all three modes

**Prerequisites**: An image loaded on canvas.

**Steps**:
1. Starting in Safe Zone mode, switch to Desktop Preview.
2. Switch from Desktop Preview to Mobile Preview.
3. Switch from Mobile Preview back to Safe Zone mode.

**Expected**: Each mode switch is smooth and instant. No console errors. The image position/zoom is preserved across mode changes (the image data is not lost). Each mode displays its distinct UI overlay correctly.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-20: Mode switching with no image loaded

**Prerequisites**: Browser open at resize-image-for-facebook-cover/index.html, no image loaded yet.

**Steps**:
1. Click the mode selector to switch to Desktop Preview (without uploading an image).
2. Click the mode selector to switch to Mobile Preview.
3. Switch back to Safe Zone mode.

**Expected**: Mode switching works even without an image loaded. Each mode shows its respective overlay/grid. No errors thrown. Upload area remains available in all modes (or the user is prompted to upload first).

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

## G. Export (TC-21 to TC-22)

### TC-21: Export as PNG (1200x628, no overlays)

**Prerequisites**: An image loaded and positioned on canvas. Image should show content extending beyond safe zone in various areas.

**Steps**:
1. Click the Export button (or select PNG format).
2. Wait for the download to begin.
3. Open the downloaded file and inspect its dimensions and content.

**Expected**: A PNG file is downloaded. Dimensions are exactly 1200x628 pixels. The image contains only the image content (no grid lines, no overlay, no UI chrome). The export reflects the current image position/zoom as it appears on the logical canvas. Download button shows "Generating..." while processing.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-22: Export as JPG (1200x628, no overlays)

**Prerequisites**: An image loaded and zoomed to 200% on canvas.

**Steps**:
1. Click the Export button and select JPG format.
2. Wait for the download to begin.
3. Open the downloaded file and inspect its dimensions and content.

**Expected**: A JPG file is downloaded. Dimensions are exactly 1200x628 pixels. No overlays (grid, UI, overlay) are present in the export. Image content matches the current canvas view (zoom level, position). File size should be smaller than equivalent PNG export.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

## H. Touch (TC-23 to TC-25)

### TC-23: Single-finger drag on touch device

**Prerequisites**: An image loaded. Device with touch input or browser touch emulation enabled.

**Steps**:
1. Touch the canvas with one finger.
2. Drag the finger across the screen.
3. Release.

**Expected**: Image pans/repositions following the finger movement (same behavior as mouse drag). One-to-one tracking. No accidental page scroll. No zoom triggered.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-24: Two-finger pinch zoom on touch device

**Prerequisites**: An image loaded. Device with touch input or Chrome DevTools touch emulation.

**Steps**:
1. Place two fingers on the canvas.
2. Pinch them together (zoom out).
3. Spread them apart (zoom in).
4. Repeat several times.

**Expected**: Image zooms in/out in response to pinch gestures. Zoom range stays within 25%-500%. The zoom change is smooth and proportional to pinch distance. No page zoom is triggered. Zoom percentage display updates in real time.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

### TC-25: Touch scroll prevention

**Prerequisites**: An image loaded. Browser DevTools touch emulation active or actual touch device.

**Steps**:
1. Outside the canvas area, scroll the page normally (verify page can scroll).
2. Place one or two fingers on the canvas area.
3. Attempt to scroll/pinch in ways that would normally scroll the page.

**Expected**: The page behind the canvas does NOT scroll when touch events occur on the canvas. `preventDefault()` is called on touch events to stop browser default behavior. The canvas captures all touch input for its own pan/zoom operations.

**Actual**: (leave empty)
**Status**: ⬜ PENDING

---

## Summary

| Section | Test Cases | Count |
|---------|-----------|-------|
| A. Upload | TC-1 to TC-4 | 4 |
| B. Drag/Zoom | TC-5 to TC-8 | 4 |
| C. Safe Zone Overlay | TC-9 to TC-11 | 3 |
| D. Desktop Immersive Preview | TC-12 to TC-15 | 4 |
| E. Mobile Immersive Preview | TC-16 to TC-18 | 3 |
| F. Mode Switching | TC-19 to TC-20 | 2 |
| G. Export | TC-21 to TC-22 | 2 |
| H. Touch | TC-23 to TC-25 | 3 |
| **Total** | | **25** |
