package=libsodium
$(package)_version=1.0.18
$(package)_download_path=https://download.libsodium.org/libsodium/releases
$(package)_file_name=libsodium-$($(package)_version).tar.gz
$(package)_sha256_hash=6f504490b342a4f8a4c4a02fc9b866cbef8622d5df4e5452b46be121e46636c1

define $(package)_config_cmds
  ./configure --with-pic="yes"
endef

define $(package)_build_cmds
  $(MAKE) $($(package)_build_opts)
endef

define $(package)_stage_cmds
  $(MAKE) DESTDIR=$($(package)_staging_dir) install
endef
