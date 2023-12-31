export * from './schemaapi.service';
import { SchemaAPI } from './schemaapi.service';
export * from './tokenapi.service';
import { TokenAPI } from './tokenapi.service';
export * from './treesapi.service';
import { TreesAPI } from './treesapi.service';
export * from './usersapi.service';
import { UsersAPI } from './usersapi.service';
export const APIS = [SchemaAPI, TokenAPI, TreesAPI, UsersAPI];
