document.addEventListener('DOMContentLoaded', () => {
  const editor = document.getElementById('editor');

  editor.addEventListener('keydown', handleKeyDown);
  editor.addEventListener('keyup', handleKeyUp);
  editor.addEventListener('input', handleInput);

  function handleKeyDown(e) {
    if (e.metaKey) {
      switch (e.key.toLowerCase()) {
        case 'b':
          e.preventDefault();
          document.execCommand('bold');
          break;
        case 'i':
          e.preventDefault();
          document.execCommand('italic');
          break;
        case 'u':
          e.preventDefault();
          document.execCommand('underline');
          break;
        case 'e':
          e.preventDefault();
          document.execCommand('formatBlock', false, 'pre');
          break;
        case 'x':
          if (e.shiftKey) {
            e.preventDefault();
            const codeText = window.getSelection().toString();
            document.execCommand(
              'insertHTML',
              false,
              `<code>${codeText}</code>`
            );
          }
          break;
      }
    }

    // Handle Tab and Shift+Tab for lists
    if (e.key === 'Tab') {
      e.preventDefault();
      const selection = window.getSelection();
      const listElement = selection.anchorNode.closest('ul, ol');
      if (listElement) {
        if (e.shiftKey) {
          document.execCommand('outdent');
        } else {
          document.execCommand('indent');
        }
      }
    }

    // Handle backspace at the beginning of elements
    if (e.key === 'Backspace') {
      const selection = window.getSelection();
      if (selection.anchorOffset === 0) {
        const parentElement = selection.anchorNode.parentElement;
        if (parentElement && parentElement.textContent.trim() === '') {
          document.execCommand('formatBlock', false, 'p');
          e.preventDefault();
        }
      }
    }
  }

  function handleKeyUp(e) {
    // Handle converting text starting with # to headings
    if (e.key === ' ') {
      const selection = window.getSelection();
      const range = selection.getRangeAt(0);
      const node = range.startContainer;
      const text = node.textContent.trim();
      if (text === '#') {
        document.execCommand('formatBlock', false, 'h1');
        node.textContent = '';
      } else if (text === '##') {
        document.execCommand('formatBlock', false, 'h2');
        node.textContent = '';
      } else if (text === '###') {
        document.execCommand('formatBlock', false, 'h3');
        node.textContent = '';
      }
    }

    // Handle bolding text with ** surrounding it
    if (e.key === ' ' || e.key === 'Enter') {
      const selection = window.getSelection();
      const range = selection.getRangeAt(0);
      const node = range.startContainer;
      const text = node.textContent;
      const boldPattern = /\*\*(.*?)\*\*/g;
      const matches = [...text.matchAll(boldPattern)];
      matches.forEach((match) => {
        const boldText = match[1];
        const newText = text.replace(`**${boldText}**`, `<b>${boldText}</b>`);
        node.textContent = '';
        document.execCommand('insertHTML', false, newText);
      });
    }
  }

  function handleInput(e) {
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    const node = range.startContainer;

    // Bullet List
    if (node.textContent.startsWith('- ')) {
      document.execCommand('insertUnorderedList');
      node.textContent = node.textContent.replace('- ', '');
    }

    // Numbered List
    if (/^\d+\.\s/.test(node.textContent)) {
      document.execCommand('insertOrderedList');
      node.textContent = node.textContent.replace(/^\d+\.\s/, '');
    }
  }
});
