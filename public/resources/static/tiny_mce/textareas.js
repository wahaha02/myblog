// tinymce_3_3_8
// O2k7 skin (black)
tinyMCE.init({
    // General options
    mode : "textareas",
    elements : "elm3",
    theme : "advanced",
    skin : "o2k7",
    skin_variant : "black",
    plugins : "safari,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
    
    // Theme options
    theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect,|,forecolor,backcolor,|,insertdate,inserttime,preview,|,link,unlink,anchor,image,cleanup,help,code",
    theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
    theme_advanced_buttons3 : "",
    theme_advanced_buttons4 : "",
    theme_advanced_toolbar_location : "top",
    theme_advanced_toolbar_align : "left",
    theme_advanced_statusbar_location : "bottom",
    theme_advanced_resizing : true,
    theme_advanced_source_editor_wrap : true,

    
    // Relative path.
    content_css : "/static/tiny_mce/css/word.css",
    theme_advanced_font_sizes: "12px,10px,13px,14px,16px,18px,20px,24px,36px",
    font_size_style_values : "12px,10px,13px,14px,16px,18px,20px,24px,36px",



});