import Vips from "../../js/lib/vips-node.mjs";

(async () => {
    try {
        const vips = await Vips();
        
        // Test ARW
        let img = vips.Image.newFromFile("rawtest/dsc1756.arw");
        console.log("ARW Loader:", img.get("vips-loader"));
        console.log("ARW Size:", img.width, "x", img.height);
        img.delete();

        // Test CR2
        img = vips.Image.newFromFile("rawtest/0c0a0435.cr2", { fail_on: "none" });
        console.log("CR2 Loader:", img.get("vips-loader"));
        console.log("CR2 Size:", img.width, "x", img.height);
        
        // Try writing CR2
        try {
            img.writeToBuffer(".jpg");
            console.log("CR2 write success");
        } catch (e) {
            console.log("CR2 write fail:", e.message);
        }
        img.delete();

        vips.shutdown();
    } catch(e) {
        console.error(e);
    }
})();
