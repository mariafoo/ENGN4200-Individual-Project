let pkgs = import /nixpkgs {}; in
{ stdenv ? pkgs.stdenv, 
  openssl ? pkgs.openssl, 
  python ? pkgs.python35, 
  numpy ? pkgs.python35Packages.numpy, 
  matplotlib ? pkgs.python35Packages.matplotlib, 
  virtualenv ? pkgs.python35Packages.virtualenv, 
  termcolor ? pkgs.python35Packages.termcolor, 
  pip ? pkgs.python35Packages.pip, 
  pyserial ? pkgs.python35Packages.pyserial
}: 

stdenv.mkDerivation {
    name = "rotational_sensor";
    src = ./.;
    propagatedBuildInputs = [ openssl python numpy matplotlib termcolor virtualenv pip pyserial ];
} 
