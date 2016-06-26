odoo.define('website_forum.website_forum',function(require){
	'use strict';

	var ajax = require('web.ajax');
	var core = require('web.core');
	var website = require('website.website');

	var _t = core._t;

	$('textarea.load_editor').each(function () {
        var $textarea = $(this);
        var $form = $textarea.closest('form');

        $('.note-editor').hide();
        $textarea.css('width','100%');
        KindEditor.ready(function(K){        	
        	window.editor=K.create($textarea,{
        		themeType:'default',
        		uploadJson : '/filemanager',
                fileManagerJson : '/filemanager',
                allowFileManager : true,
        	})
        });
        $form.off('click');

        $form.on('click', 'button, .a-submit', function () {
            window.editor.sync();
            window.editor.html($textarea.val());
        });
    });

})