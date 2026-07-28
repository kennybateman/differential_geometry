let 
  home = builtins.getEnv "HOME";
  version = (import "${home}/Desktop/differential_geometry/nixpkgs.nix").july_27_2026_;

in
  { nixpkgs ? import version {} }:

    let
      packages = [
        # Ruby language
        nixpkgs.ruby
        nixpkgs.bundix # nix style gemset management

        # Rails support
        nixpkgs.nodejs # for js asset bundling
        nixpkgs.sqlite # database

        # Python language
        nixpkgs.python312
        nixpkgs.uv # python package and environment manager

        # General language support
        nixpkgs.gcc        # c-compiling
        nixpkgs.openssl    # networking
        nixpkgs.zlib       # compression
        nixpkgs.libffi     # for foreign function interfaces
        nixpkgs.libyaml    # for faster YAML parsing
        nixpkgs.pkg-config # for building native extensions
        nixpkgs.libxml2
        nixpkgs.libxslt
        nixpkgs.yarn

        nixpkgs.openblas
        nixpkgs.stdenv.cc.cc.lib
      ];

    in nixpkgs.mkShell {
      inherit packages;

    LD_LIBRARY_PATH = nixpkgs.lib.makeLibraryPath [
        nixpkgs.zlib
        nixpkgs.openblas
        nixpkgs.stdenv.cc.cc.lib
    ];

    shellHook = ''
      # Print out the packages in the nix shell to a file for easy reference
      rm nix.txt 2>/dev/null # delete old file if exists
      ${builtins.concatStringsSep "\n"
        (map (p: "echo ${p.pname or p.name} ${p.version or ""} >> nix.txt" ) packages)}
    '';
  }