{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";
    pre-commit-hooks.url = "github:cachix/git-hooks.nix";
  };
  outputs = { self, nixpkgs, ... }@inputs:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
        inherit system;
      });
    in
    {
      checks = forEachSupportedSystem
        ({ pkgs, system, ... }: {
          pre-commit-check = inputs.pre-commit-hooks.lib.${system}.run
            {
              src = ./.;
              hooks = {
                mypy = {
                  enable = true;
                  excludes = [ "tests" ];
                  extraPackages = with pkgs.python312Packages; [
                    types-toml
                  ];
                };
                ruff = {
                  enable = true;
                  excludes = [ "tests" ];
                  package = pkgs.ruff;
                };
                ruff-format = {
                  enable = true;
                  package = pkgs.ruff;
                };
              };
            };
        });
      devShells = forEachSupportedSystem ({ pkgs, system }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            python312
            uv
          ] ++
          (with pkgs.python312Packages; [
            pip
            virtualenvwrapper
          ]);
          shellHook = self.checks.${system}.pre-commit-check.shellHook + ''
            VENV=.venv
            if test ! -d $VENV; then
              virtualenv $VENV
            fi
            source $VENV/bin/activate
            export PYTHONPATH=`pwd`/$VENV/${pkgs.python312.sitePackages}:$PYTHONPATH
          '';
          buildInputs = self.checks.${system}.pre-commit-check.enabledPackages;
        };
      });
    };
}
