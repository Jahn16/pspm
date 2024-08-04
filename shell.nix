{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  venvDir = ".venv";
  packages = with pkgs; [ python312 ] ++
    (with pkgs.python312Packages; [
      pip
      venvShellHook
      uv
    ]);
}
