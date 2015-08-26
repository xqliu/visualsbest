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
                    '<li><div>', '<img src="', e.target.result, '"/>', '</div></li>'
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

    $("#images-preview-panel").find("li div span").click(function (event) {
        if (confirm('确定从当前作品集中删除本作品吗?')) {
            var id = event.target.id.slice('delete-'.length);
            var photo_works_to_del_var = $("#photo-works-to-delete");
            if (photo_works_to_del_var.val() === '') {
                photo_works_to_del_var.val(id);
            } else {
                photo_works_to_del_var.val(
                        photo_works_to_del_var.val() + ',' + id
                );
            }
            $("#photo-work-" + id).hide(500);
        }
    });
});
