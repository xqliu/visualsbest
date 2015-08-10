function handleFileSelect(evt) {
    var files = evt.target.files;
    // Loop through the FileList and render image files as thumbnails.
    for (var i = 0, f; f = files[i]; i++) {
        // Only process image files.
        if (!f.type.match('image.*')) {
            continue;
        }
        var reader = new FileReader();
        // Closure to capture the file information.
        reader.onload = (function (theFile) {
            return function (e) {
                // Render thumbnail.
                var span = document.createElement('span');
                span.innerHTML = [
                    '<li><div>', '<img src="', e.target.result, '"/>', '<span></span>', '</div></li>'
                ].join('');
                document.getElementById('images-preview-panel').insertBefore(span, null);
            };
        })(f);
        // Read in the image file as a data URL.
        reader.readAsDataURL(f);
    }
}
document.getElementById('photo_collection_files').addEventListener('change', handleFileSelect, false);

// 在edit_photo_collection 页面，点击就弹出选择文件的对话框
$(function () {
    $("#upload_files_trigger_image").click(function () {
        $("input[id='photo_collection_files']").click();
    });
    $("#upload_files_trigger_text").click(function () {
        $("input[id='photo_collection_files']").click();
    });
});