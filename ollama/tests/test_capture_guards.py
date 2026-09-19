from pathlib import Path
import os
from types import SimpleNamespace
import sys
import pytest
from ollama_usage_grabber import capture


@pytest.mark.skipif(os.name != "nt", reason="Desktop capture is Windows-only")
def test_existing_capture_stops_before_desktop_actions(tmp_path,monkeypatch):
    (tmp_path/'ollama_settings_window.png').write_bytes(b'preserved fixture')
    for name in ('pyautogui','pytesseract'):
        monkeypatch.setitem(sys.modules,name,SimpleNamespace())
    monkeypatch.setitem(sys.modules,'PIL',SimpleNamespace(Image=SimpleNamespace(),ImageGrab=SimpleNamespace()))
    def forbidden(*args,**kwargs):raise AssertionError('Attempted desktop action')
    monkeypatch.setattr(capture.webbrowser,'open_new',forbidden)
    with pytest.raises(FileExistsError):capture.capture_usage(tmp_path)
    assert (tmp_path/'ollama_settings_window.png').read_bytes()==b'preserved fixture'


def test_foreground_mismatch_stops_before_action(monkeypatch):
    import ctypes
    class Function:
        def __init__(self,run):self.run=run
        def __call__(self,*args):return self.run(*args)
    def title(window,buffer,length):buffer.value='Unrelated application';return 21
    api=SimpleNamespace(GetForegroundWindow=Function(lambda:123),GetWindowTextLengthW=Function(lambda _:21),GetWindowTextW=Function(title))
    monkeypatch.setattr(ctypes,'windll',SimpleNamespace(user32=api),raising=False)
    with pytest.raises(RuntimeError,match='foreground'):
        capture._require_foreground_title('Expected Capture')
