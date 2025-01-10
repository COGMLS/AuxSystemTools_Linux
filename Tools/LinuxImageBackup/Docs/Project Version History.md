# Linux Image Backup: Version History:

This document contain the complete change history to Linux Image Backup

## Linux Image Backup History:

<!-- Linux Image Backup History Table: -->
<style>
    version-data
    {
        font-weight: bold;
    }
    fix-alert
    {
        font-weight: bold;
    }
    bug-alert
    {
        font-weight: bold;
        color: red;
    }
    warning-alert
    {
        font-weight: bold;
        color: orange;
    }
    note-alert
    {
        font-weight: bold;
    }
</style>
<dl>
    <!-- 0.2.0-alpha.1 (2025/01/10) -->
    <dt><version-data>0.2.0-alpha.1</version-data></dt>
    <dd>Added <code>mount_point</code> class</dd>
    <dd>Added fstab methods</dd>
    <dd>Added <code>getAutoMountPoints</code> to get automated mount points in fstab file</dd>
    <dd>Added auxiliary methods for fstab</dd>
    <dd>Added <code>DISK_UUID_PATH</code> definition</dd>
    <dd><fix-alert>[FIX]</fix-alert> string copy of version type</dd>
    <!-- 0.2.0-alpha.1 (2025/01/09) -->
    <dt><version-data>0.2.0-alpha.1</version-data></dt>
    <dd>Added <code>device_index</code> to identify the device index. I.e. sda1 to <code>DeviceUuid</code></dd>
    <dd>Added index method to get <code>device_index</code> value to <code>DeviceUuid</code></dd>
    <dd>Added error handling class</dd>
    <dd>Added error messages</dd>
    <dd>Added exceptions to <code>storage_device</code> class</dd>
    <dd>Added sort algorithm, to organize the UUID devices by their indexes</dd>
    <dd>Added new constructors to <code>storage_device</code></dd>
    <!-- 0.2.0-alpha (2025/01/07) -->
    <dt><version-data>0.2.0-alpha</version-data></dt>
    <dd>Added the functions definitions to <code>FileTools</code></dd>
    <dd>Added parameter <code>ignoreFilePerms</code> when try to read/write the file to <code>FileTools</code></dd>
    <dd>Added assign operators</dd>
    <dd>Changed datatype to getPath method to <code>storage_device</code></dd>
    <dd><fix-alert>[FIX]</fix-alert> bug that does not read the device files in <code>storage_device</code> constructor</dd>
    <dd>Implemented other methods to <code>storage_device</code>.</dd>
    <!-- 0.1.0-alpha (2025/01/04) -->
    <dt><version-data>0.1.0-alpha</version-data></dt>
    <dd>Added <code>DeviceUuid</code> class</dd>
    <dd><fix-alert>[FIX]</fix-alert> use of <code>nullptr</code> with <code>c_uuid_str</code>.</dd>
    <dd>Now convert direct the <code>uuid_str</code> object.</dd>
    <dd>Simplified the definition of <code>hasRootRights</code> to <code>FileTools</code></dd>
    <dd>Added default constructor for <code>DeviceUuid</code>.</dd>
    <dd>Minor changes on using how to convert the path data into strings.</dd>
    <dd>Added <code>FileTools</code></dd>
    <dd>Added declarations of new methods to <code>storage_device</code></dd>
    <dd>Added new private variables to <code>storage_device</code></dd>
    <dd>Added <code>storage_device</code> constructor</dd>
    <!-- 0.0.1-alpha.2 (2025/01/03) -->
    <dt><version-data>0.0.1-alpha.2</version-data></dt>
    <dd>Added <code>DateTimeInfo</code> class</dd>
    <dd>Added system tools methods</dd>
    <!-- 0.0.1-alpha (2024/12/28 - 2025/01/02) -->
    <dt><version-data>0.0.1-alpha</version-data></dt>
    <dd>Added the basic console structure for user interactions</dd>
    <dd>Added main.cpp</dd>
    <dd>Added custom C++ exceptions.</dd>
    <dd>Added ConsoleOutput components.</dd>
    <dd>Added Version information.</dd>
    <dd>Added .gitignore file.</dd>
    <dd>Added ImageBackup components.</dd>
    <dd>Added DiskTools components</dd>
    <dd><note-alert>NOTE: The project is under development and some components are incomplete.</note-alert></dd>
</dl>
