let
  downloadFromGithub = { version, name, owner, sha256 }:
    builtins.fetchTarball {
      name = "${name}-${version}";
      url = "https://github.com/${owner}/${name}/archive/${version}.tar.gz";
      inherit sha256;
    };
in
{
  # Use the date you started using it, not the date of the commit, as a variable name
  july_27_2026_ = downloadFromGithub {
    version = "8c50a71"; # https://github.com/NixOS/nixpkgs/commit/8c50a710ddca43d7a530fb805ad55bde8d0141c5
    owner = "NixOS";
    name = "nixpkgs";
    sha256 = "0am8xx09fx5yf2p0wb001v0jx1g5hrfb76h4r37xph378jgk7pcr";
  };
}