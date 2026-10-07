# Preserve UTF-8 strings without transcoding through a Windows C locale.
read_registry <- function(path) {
  yaml::yaml.load(paste(readLines(path, encoding = "UTF-8", warn = FALSE), collapse = "\n"))
}
